import time
import threading
import os
import subprocess
import re
import datetime
import logging
import typing

import git
import git.exc
import filelock

from .data import User, Function
from .state import State
from .errors import MetadataNotFoundError
from .utils import is_py3

_l = logging.getLogger(name=__name__)
BINSYNC_BRANCH_PREFIX = 'binsync'
BINSYNC_ROOT_BRANCH = f'{BINSYNC_BRANCH_PREFIX}/__root__'


class ConnectionWarnings:
    HASH_MISMATCH = 0


class StateContext(object):
    def __init__(self, client, state, locked=False):
        self.client = client
        self.state = state
        self.locked = locked

    def __enter__(self):
        if self.locked:
            self.client.commit_lock.acquire()
        return self.state

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.locked:
            self.client.commit_lock.release()
        self.client.save_state(state=self.state)


class Client(object):
    """
    The binsync Client.

    :ivar str master_user:  User name of the master user.
    :ivar str repo_root:    Local path of the Git repo.
    :ivar str remote:       Git remote.
    :ivar int _commit_interval: The interval for committing local changes into the Git repo, pushing to the remote
                            side, and pulling from the remote.
    """

    def __init__(
        self,
        master_user,
        repo_root,
        binary_hash,
        remote="origin",
        commit_interval=10,
        init_repo=False,
        remote_url=None,
        ssh_agent_pid=None,
        ssh_auth_sock=None,
        last_push_func=-1,
        last_push_time=-1,
    ):
        """
        :param str master_user:     The username of the current user
        :param str repo_root:       The path to the repository directory to be loaded or created
        :param str binary_hash:     The binary's md5 hash, as a hex string, for validation
        :param remote:
        :param commit_interval:
        :param init_repo:
        :param remote_url:
        :param ssh_agent_pid:
        :param ssh_auth_sock:
        """
        self.master_user = master_user
        self.repo_root = repo_root
        self.binary_hash = binary_hash
        self.remote = remote
        self.repo = None
        self.repo_lock = None

        if master_user.endswith('/') or '__root__' in master_user:
            raise Exception(f"Bad username: {master_user}")

        # ssh-agent info
        self.ssh_agent_pid = ssh_agent_pid  # type: int
        self.ssh_auth_sock = ssh_auth_sock  # type: str
        self.connection_warnings = []

        # three scenarios
        # 1. We already have the repo checked out
        # 2. We haven't checked out the repo, but there is a remote repo. In this case, we clone the repo from
        #    @remote_url
        # 3. There is no such repo, and we are the very first group of people trying to setup this repo. In this case,
        #    @init_repo should be True, and we will initialize the repo.

        try:
            # case 1
            # open the local repo
            self.repo = git.Repo(self.repo_root)

            # Initialize branches
            self.init_remote()

            if init_repo:
                raise Exception("Could not initialize repository - it already exists!")
            if not any(b.name == BINSYNC_ROOT_BRANCH for b in self.repo.branches):
                raise Exception(f"This is not a binsync repo - it must have a {BINSYNC_ROOT_BRANCH} branch.")
        except (git.NoSuchPathError, git.InvalidGitRepositoryError):
            # initialization
            if remote_url:
                # case 2
                self.repo = self.clone(remote_url)
            elif init_repo:
                # case 3
                self.repo = git.Repo.init(self.repo_root)
                self._setup_repo()
            else:
                raise

        stored = self._get_stored_hash()
        if stored != binary_hash:
            self.connection_warnings.append(ConnectionWarnings.HASH_MISMATCH)

        assert not self.repo.bare, "it should not be a bare repo"

        self.repo_lock = filelock.FileLock(self.repo_root + "/.git/binsync.lock")
        try:
            self.repo_lock.acquire(timeout=0)
        except filelock.Timeout as e:
            raise Exception("Can only have one binsync client touching a local repository at once.\n"
                            "If the previous client crashed, you need to delete " + self.repo_root + "/.git/binsync.lock") from e

        # check out the appropriate branch
        try:
            branch = next(o for o in self.repo.branches if o.name.endswith(self.user_branch_name))
        except StopIteration:
            branch = self.repo.create_head(self.user_branch_name, BINSYNC_ROOT_BRANCH)
        else:
            if branch.is_remote():
                branch = self.repo.create_head(self.user_branch_name)
        branch.checkout()

        self._commit_interval = commit_interval
        self._worker_thread = None
        self._last_push_at = None  # type: datetime.datetime
        self._last_push_attempt_at = None  # type: datetime.datetime
        self._last_pull_at = None  # type: datetime.datetime
        self._last_pull_attempt_at = None  # type: datetime.datetime

        # User last push time/function
        self.last_push_time = -1
        self.last_push_function = -1

        # timestamps
        self._last_commit_ts = 0

        self.state = None
        self.commit_lock = threading.Lock()

    def init_remote(self):
        """
        Init PyGits view of remote references in a repo. If the remote can not be found,
        exit early.

        """
        # Get all branches
        try:
            branches = self.repo.remote().refs
        except ValueError:
            return

        # Iterate over all branches, track commits
        for branch in branches:
            # Yeet head
            if "HEAD" in branch.name:
                continue
            # Checkout and track
            try:
                self.repo.git.checkout('--track', branch.name)
            except git.GitCommandError as e:
                pass

    def __del__(self):
        if self.repo_lock is not None:
            self.repo_lock.release()

    @property
    def user_branch_name(self):
        return f"{BINSYNC_BRANCH_PREFIX}/{self.master_user}"

    @property
    def has_remote(self):
        """
        If there is a remote configured for our local repo.

        :return:    True if there is a remote, False otherwise.
        """
        return self.remote and self.repo.remotes and any(r.name == self.remote for r in self.repo.remotes)

    @property
    def last_update_timestamp(self):
        return self._last_commit_ts

    def ssh_agent_env(self):
        if self.ssh_agent_pid is not None and self.ssh_auth_sock is not None:
            env = {
                'SSH_AGENT_PID': str(self.ssh_agent_pid),
                'SSH_AUTH_SOCK': str(self.ssh_auth_sock),
            }
        else:
            env = { }
        return env

    def add_remote(self, name, remote_url):
        """
        Add a remote to the local repo.

        :param name:
        :param remote_url:
        :return:
        """

        self.repo.create_remote(name, url=remote_url)

    def clone(self, remote_url):
        """
        Checkout from a remote_url to a local path specified by self.local_root.

        :param str remote_url:  The URL of the Git remote.
        :return:                None
        """

        env = self.ssh_agent_env()
        repo = git.Repo.clone_from(remote_url, self.repo_root, env=env)

        try:
            repo.create_head(BINSYNC_ROOT_BRANCH, f'{self.remote}/{BINSYNC_ROOT_BRANCH}')
        except git.BadName:
            raise Exception(f"This is not a binsync repo - it must have a {BINSYNC_ROOT_BRANCH} branch")

        return repo

    def pull(self, print_error=False):
        """
        Pull changes from the remote side.

        :return:    None
        """

        self._last_pull_attempt_at = datetime.datetime.now()

        if self.has_remote:
            try:
                env = self.ssh_agent_env()
                with self.repo.git.custom_environment(**env):
                    self.repo.remotes[self.remote].pull()
                self._last_pull_at = datetime.datetime.now()
            except git.exc.GitCommandError as ex:
                if print_error:
                    print("Failed to pull from remote \"%s\".\n"
                          "\n"
                          "Git error: %s." % (
                              self.remote,
                              str(ex)
                          ))

    def push(self, print_error=False):
        """
        Push local changes to the remote side.

        :return:    None
        """

        self._last_push_attempt_at = datetime.datetime.now()

        if self.has_remote:
            try:
                env = self.ssh_agent_env()
                with self.repo.git.custom_environment(**env):
                    self.repo.remotes[self.remote].push(BINSYNC_ROOT_BRANCH)
                    self.repo.remotes[self.remote].push(self.user_branch_name)
                self._last_push_at = datetime.datetime.now()
            except git.exc.GitCommandError as ex:
                if print_error:
                    print("Failed to push to remote \"%s\".\n"
                          "Did you setup %s/master as the upstream of the local master branch?\n"
                          "\n"
                          "Git error: %s." % (
                        self.remote,
                        self.remote,
                        str(ex)
                    ))

    def users(self) -> typing.Iterable[User]:
        for ref in self._get_best_refs():
            try:
                metadata = State.load_metadata(ref.commit.tree)
                yield User.from_metadata(metadata)
            except Exception as e:
                continue

    def tally(self, users=None):
        """
        Return a dict of user names and what information they can provide, e.g.,
        {"user":
            {
                "functions": [0x400080],
            }
        }

        :param list users:  A list of user names or None if we don't want to limit the range of user names we care about.
        :return:            A dict with tally information.
        :rtype:             dict
        """

        if users is not None:
            users = set(users)
        else:
            users = [x.name for x in self.users()]

        all_info = {}

        for user in self.users():
            if user is None or user.name not in users:
                continue

            # what information does this user provide?
            info = {}
            state = self.get_state(user=user.name)
            info["function"] = list(state.functions.keys())
            #info["comments"] = list(state.comments.keys())
            info["patches"] = list(
                {"obj_name": p.obj_name, "offset": p.offset}
                for p in state.patches.values()
            )

            all_info[user.name] = info

        return all_info

    def status(self):
        """
        Return a dict of status information.
        """

        d = {}

        d['remote_name'] = self.remote

        if self.repo is not None:
            d['last_commit_hash'] = self.repo.heads[0].commit.hexsha
            try:
                d['last_commit_time'] = self.repo.heads[0].commit.committed_datetime.replace(tzinfo=None)
            except IOError:  # sometimes GitPython throws this exception
                d['last_commit_time'] = "<unknown>"
            if any(r.name == self.remote for r in self.repo.remotes):
                d['remote_url'] = ";".join(self.repo.remotes[self.remote].urls)
            else:
                d['remote_url'] = "<does not exist>"

            d['last_change'] = self._last_push_at if self._last_push_at is not None else "never"
            d['last_push_attempt'] = self._last_push_attempt_at if self._last_push_attempt_at is not None else "never"
            d['last_pull'] = self._last_pull_at if self._last_pull_at is not None else "never"
            d['last_pull_attempt'] = self._last_pull_attempt_at if self._last_pull_attempt_at is not None else "never"

        return d

    def state_ctx(self, user=None, version=None, locked=False):
        state = self.get_state(user=user, version=version)
        return StateContext(self, state, locked=locked)

    def get_tree(self, user):
        options = [ref for ref in self.repo.refs if ref.name.endswith(f"{BINSYNC_BRANCH_PREFIX}/{user}")]
        if not options:
            raise ValueError(f'No such user "{user}" found in repository')
        best = max(options, key=lambda ref: ref.commit.authored_date)
        return best.commit.tree

    def get_state(self, user=None, version=None):
        if user is None or user == self.master_user:
            # local state
            if self.state is None:
                try:
                    self.state = State.parse(
                        self.get_tree(user=self.master_user), version=version,
                        client=self,
                    )  # Also need to check if user is none here???
                except MetadataNotFoundError:
                    # we should return a new state
                    self.state = State(user if user is not None else self.master_user, client=self)
            return self.state
        else:
            try:
                state = State.parse(self.get_tree(user=user), version=version, client=self)
                return state
            except MetadataNotFoundError:
                return None

    def get_locked_state(self, user=None, version=None):
        with self.commit_lock:
            yield self.get_state(user=user, version=version)

    def start_auto(self):
        if self._worker_thread is None:
            self._worker_thread = threading.Thread(target=self._worker_routine)
            self._worker_thread.start()
        else:
            raise Exception(
                "start_auto() should not be called twice. There is already a worker thread running."
            )

    def _worker_routine(self):
        while True:
            time.sleep(self._commit_interval)
            self.update()

    def update(self):
        """

        :return:
        """

        # do a pull... if there is a remote
        if self.has_remote:
            self.pull()

        #print("IS DIRTY??", self.get_state().dirty)
        if self.get_state().dirty:
            # do a save!
            self.save_state()

        if self.has_remote:
            # do a push... if there is a remote
            self.push()

        self._last_commit_ts = time.time()

    def set_last_push(self, func_addr: int, push_time: int, func_name: str):
        """
        Setter for the push variables.
        """
        state = self.get_state(user=self.master_user)

        # update a users global metadata
        state.last_push_func = func_addr
        state.last_push_time = push_time

        # create a function if it does not exist in this users state
        try:
            changed_func = state.get_function(func_addr)
        except KeyError:
            changed_func = Function(func_addr)

        # update a users local, function level, metadata
        changed_func.last_change = push_time
        changed_func.name = func_name
        state.set_function(changed_func)

    def save_state(self, state=None):

        if state is None:
            state = self.state

        # you don't want to save as another user... unless you want to mess things up for your collaborators, in which
        # case, please comment out the following assertion.
        assert self.master_user == state.user

        branch = next(o for o in self.repo.branches if o.name == self.user_branch_name)
        index = self.repo.index

        self.commit_lock.acquire()
        # dump the state
        state.dump(index)

        # commit changes
        self.repo.index.add([os.path.join(state.user, "*")])
        self.commit_lock.release()

        if self.repo.index.diff("HEAD"):
            # commit if there is any difference
            commit = index.commit("Save state")
            branch.commit = commit
            self.push()

    def sync_states(self, user=None):
        target_state = self.get_state(user)
        if target_state == None:
            print("Unable to find state for user", user)
            return

        my_state = self.get_state(self.master_user)

        my_state.copy_state(target_state)
        self.save_state()    

    @staticmethod
    def discover_ssh_agent(ssh_agent_cmd):
        proc = subprocess.Popen(ssh_agent_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()

        if is_py3:
            stdout = stdout.decode("utf-8")
            stderr = stderr.decode("utf-8")

        if proc.returncode != 0 or stderr:
            raise RuntimeError("Failed to discover SSH agent by running command %s.\n"
                               "Return code: %d.\n"
                               "stderr: %s" % (
                ssh_agent_cmd,
                proc.returncode,
                stderr,
            ))

        # parse output
        m = re.search(r"Found ssh-agent at (\d+)", stdout)
        if m is None:
            return None, None
        ssh_agent_pid = int(m.group(1))

        m = re.search(r"Found ssh-agent socket at ([^\s]+)", stdout)
        if m is None:
            return None, None
        ssh_agent_sock = m.group(1)

        return ssh_agent_pid, ssh_agent_sock

    def close(self):
        self.repo.close()
        del self.repo

    def _get_best_refs(self):
        candidates = {}
        for ref in self.repo.refs:  # type: git.Reference
            if f'{BINSYNC_BRANCH_PREFIX}/' not in ref.name:
                continue

            branch_name = ref.name.split("/")[-1]
            if branch_name in candidates:
                # if the candidate exists, and the new one is not remote, don't replace it
                if not ref.is_remote() or ref.remote_name != self.remote:
                    continue

            candidates[branch_name] = ref
        return candidates.values()

    def _setup_repo(self):
        with open(os.path.join(self.repo_root, ".gitignore"), "w") as f:
            f.write(".git/*\n")
        with open(os.path.join(self.repo_root, "binary_hash"), "w") as f:
            f.write(self.binary_hash)
        self.repo.index.add([".gitignore", "binary_hash"])
        self.repo.index.commit("Root commit")
        self.repo.create_head(BINSYNC_ROOT_BRANCH)

    def _get_stored_hash(self):
        branch = [ref for ref in self.repo.refs if ref.name.endswith(BINSYNC_ROOT_BRANCH)][0]
        return branch.commit.tree["binary_hash"].data_stream.read().decode().strip("\n")
