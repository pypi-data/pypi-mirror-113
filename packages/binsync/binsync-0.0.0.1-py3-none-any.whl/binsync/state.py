try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

import os
from functools import wraps
from collections import defaultdict
import pathlib

from sortedcontainers import SortedDict
import toml
import git

from .data import Function, Comment, Patch, StackVariable
from .data.struct import Struct
from .errors import MetadataNotFoundError
from .utils import is_py2, is_py3

if is_py3():
    from typing import Dict, TYPE_CHECKING, Optional
    if TYPE_CHECKING:
        from .client import Client


def dirty_checker(f):
    @wraps(f)
    def dirtycheck(self, *args, **kwargs):
        r = f(self, *args, **kwargs)
        if r is True:
            self._dirty = True
        return r

    return dirtycheck

def list_files_in_tree(base_tree: git.Tree):
    """
    Lists all the files in a repo at a given tree

    :param commit: A gitpython Tree object
    """

    file_list = []
    stack = [base_tree]
    while len(stack) > 0:
        tree = stack.pop()
        # enumerate blobs (files) at this level
        for b in tree.blobs:
            file_list.append(b.path)
        for subtree in tree.trees:
            stack.append(subtree)

    return file_list


def add_data(index: git.IndexFile, path: str, data: bytes):
    fullpath = os.path.join(os.path.dirname(index.repo.git_dir), path)
    pathlib.Path(fullpath).parent.mkdir(parents=True, exist_ok=True)
    with open(fullpath, 'wb') as fp:
        fp.write(data)
    index.add([fullpath])


def remove_data(index: git.IndexFile, path: str):
    fullpath = os.path.join(os.path.dirname(index.repo.git_dir), path)
    pathlib.Path(fullpath).parent.mkdir(parents=True, exist_ok=True)
    index.remove([fullpath], working_tree=True)


class State:
    """
    The state.

    :ivar str user:     Name of the user.
    :ivar int version:  Version of the state, starting from 0.
    """

    def __init__(self, user, version=None, client=None):
        # metadata info
        self.user = user  # type: str
        self.version = version if version is not None else 0  # type: int
        self.last_push_func = -1
        self.last_push_time = -1

        # the client
        self.client = client  # type: Optional[Client]

        # dirty bit
        self._dirty = True  # type: bool

        # data
        self.functions = {}  # type: Dict[int, Function]
        self.comments = defaultdict(dict)  # type: Dict[int, Dict[int, Comment]]
        self.stack_variables = defaultdict(dict)  # type: Dict[int, Dict[int, StackVariable]]
        self.structs = defaultdict()  # type: Dict[str, Struct]
        self.patches = SortedDict()

    @property
    def dirty(self):
        return self._dirty

    def ensure_dir_exists(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        if not os.path.isdir(dir_name):
            raise RuntimeError("Cannot create directory %s. Maybe it conflicts with an existing file?" % dir_name)

    def dump_metadata(self, index):
        d = {
            "user": self.user,
            "version": self.version,
            "last_push_func": self.last_push_func,
            "push_time": self.last_push_time
        }
        add_data(index, 'metadata.toml', toml.dumps(d).encode())

    def dump(self, index: git.IndexFile):
        # dump metadata
        self.dump_metadata(index)

        # dump function
        add_data(index, 'functions.toml', toml.dumps(Function.dump_many(self.functions)).encode())

        # dump patches
        add_data(index, 'patches.toml', toml.dumps(Patch.dump_many(self.patches)).encode())

        # dump comments, one file per function
        for func_addr, cmts in self.comments.items():
            path = os.path.join('comments', "%08x.toml" % func_addr)
            add_data(index, path, toml.dumps(Comment.dump_many(cmts)).encode())

        # dump stack variables, one file per function
        for func_addr, stack_vars in self.stack_variables.items():
            path = os.path.join('stack_vars', "%08x.toml" % func_addr)
            add_data(index, path, toml.dumps(StackVariable.dump_many(stack_vars)).encode())

        # dump structs, one file per struct
        for s_name, struct in self.structs.items():
            path = os.path.join('structs', f"{s_name}.toml")
            add_data(index, path, toml.dumps(struct.dump()).encode())

    @staticmethod
    def load_metadata(tree):
        return toml.loads(tree['metadata.toml'].data_stream.read().decode())

    @classmethod
    def parse(cls, tree: git.Tree, version=None, client=None):
        s = cls(None, client=client)

        # load metadata
        try:
            metadata = cls.load_metadata(tree)
        except:
            # metadata is not found
            raise MetadataNotFoundError()
        s.user = metadata["user"]

        s.version = version if version is not None else metadata["version"]

        # load function
        try:
            funcs_toml = toml.loads(tree['functions.toml'].data_stream.read().decode())
        except:
            pass
        else:
            functions = {}
            for func in Function.load_many(funcs_toml):
                functions[func.addr] = func
            s.functions = functions

        # load comments
        for func_addr in s.functions:
            try:
                # TODO use unrebased address for more durability
                cmts_toml = toml.loads(tree[os.path.join('comments', '%08x.toml' % func_addr)].data_stream.read().decode())
            except:
                pass
            else:
                cmts = list(Comment.load_many(cmts_toml))
                d = dict((c.addr, c) for c in cmts)
                if cmts:
                    s.comments[cmts[0].func_addr] = d

        # load patches
        try:
            patches_toml = toml.loads(tree['patches.toml'].data_stream.read().decode())
        except:
            pass
        else:
            patches = {}
            for patch in Patch.load_many(patches_toml):
                patches[patch.offset] = patch
            s.patches = SortedDict(patches)

        # load stack variables
        for func_addr in s.functions:
            try:
                # TODO use unrebased address for more durability
                svs_toml = toml.loads(tree[os.path.join('stack_vars', '%08x.toml' % func_addr)].data_stream.read().decode())
            except:
                pass
            else:
                svs = list(StackVariable.load_many(svs_toml))
                d = dict((v.stack_offset, v) for v in svs)
                if svs:
                    s.stack_variables[svs[0].func_addr] = d

        # load structs
        tree_files = list_files_in_tree(tree)
        struct_files = [name for name in tree_files if name.startswith("structs")]
        for struct_file in struct_files:
            try:
                struct_toml = toml.loads(tree[struct_file].data_stream.read().decode())
            except:
                pass
            else:
                struct = Struct.load(struct_toml)
                s.structs[struct.name] = struct

        # clear the dirty bit
        s._dirty = False

        return s

    def copy_state(self, target_state=None):
        if target_state is None:
            print("Cannot copy an empty state (state == None)")
            return

        self.functions = target_state.functions.copy()
        self.comments = target_state.comments.copy()
        self.stack_variables = target_state.stack_variables.copy()
        self.patches = target_state.patches.copy()
        self.structs = target_state.structs.copy()
        
    def save(self):
        if self.client is None:
            raise RuntimeError("save(): State.client is None.")
        self.client.save_state(self)

    #
    # Pushers
    #

    @dirty_checker
    def update_metadata(self, last_func_push: str, last_push_time: int):
        pass


    @dirty_checker
    def set_function(self, func):

        if not isinstance(func, Function):
            raise TypeError(
                "Unsupported type %s. Expecting type %s." % (type(func), Function)
            )

        if func.addr in self.functions and self.functions[func.addr] == func:
            # no update is required
            return False

        self.functions[func.addr] = func
        return True

    @dirty_checker
    def set_comment(self, comment: Comment):

        if comment and \
                comment.func_addr in self.comments and \
                comment.addr in self.comments[comment.func_addr] and \
                self.comments[comment.func_addr][comment.addr] == comment:
            # no update is required
            return False

        self.comments[comment.func_addr][comment.addr] = comment
        return True

    @dirty_checker
    def remove_comment(self, func_addr, addr):
        try:
            del self.comments[func_addr][addr]
            return True
        except KeyError:
            return False

    @dirty_checker
    def set_patch(self, addr, patch):

        if addr in self.patches and self.patches[addr] == patch:
            # no update is required
            return False

        self.patches[addr] = patch
        return True

    @dirty_checker
    def set_stack_variable(self, func_addr, offset, variable):
        if func_addr in self.stack_variables \
                and offset in self.stack_variables[func_addr] \
                and self.stack_variables[func_addr][offset] == variable:
            # no update is required
            return False

        self.stack_variables[func_addr][offset] = variable
        return True

    @dirty_checker
    def set_struct(self, struct: Struct, old_name: str):
        """
        Sets a struct in the current state. If old_name is not defined (None), then
        this indicates that the struct has not changed names. In that case, simply overwrite the
        internal representation of the struct.

        If the old_name is defined, than a struct has changed names. In that case, delete
        the internal struct data and delete the related .toml file.

        @param struct:
        @param old_name:
        @return:
        """
        if struct.name in self.structs \
                and self.structs[struct.name] == struct:
            # no updated is required
            return False

        # delete old struct only when we know what it is
        if old_name is not None:
            try:
                del self.structs[old_name]
                # delete the repo toml for the struct
                remove_data(self.client.repo.index, os.path.join('structs', f'{old_name}.toml'))
            except KeyError:
                pass

        # set the new struct
        if struct.name is not None:
            self.structs[struct.name] = struct

    #
    # Pullers
    #

    def get_function(self, addr):

        if addr not in self.functions:
            raise KeyError("Function %x is not found in the db." % addr)

        return self.functions[addr]

    def get_comment(self, func_addr, addr):
        if func_addr not in self.comments:
            raise KeyError("There is no comment at address %#x." % addr)

        if addr not in self.comments[func_addr]:
            raise KeyError("There is no comment at address %#x." % addr)

        cmt = self.comments[func_addr][addr]
        return cmt

    def get_comments(self, func_addr):
        if func_addr not in self.comments:
            raise KeyError("There is no comment at address %#x." % func_addr)

        return self.comments[func_addr]

    def get_patch(self, addr):

        if addr not in self.patches:
            raise KeyError("There is no patch at address %#x." % addr)

        return self.patches[addr]

    def get_patches(self):
        return self.patches.values()

    def get_stack_variable(self, func_addr, offset):
        if func_addr not in self.stack_variables:
            raise KeyError("No stack variables are defined for function %#x." % func_addr)
        if offset not in self.stack_variables[func_addr]:
            raise KeyError("No stack variable exists at offset %d in function %#x." % (offset, func_addr))
        return self.stack_variables[func_addr][offset]

    def get_stack_variables(self, func_addr):
        if func_addr not in self.stack_variables:
            raise KeyError("No stack variables are defined for function %#x." % func_addr)
        return self.stack_variables[func_addr].items()

    def get_struct(self, struct_name):
        if struct_name not in self.structs:
            raise KeyError(f"No struct by the name {struct_name} defined.")
        return self.structs[struct_name]

    def get_structs(self):
        return self.structs.values()

