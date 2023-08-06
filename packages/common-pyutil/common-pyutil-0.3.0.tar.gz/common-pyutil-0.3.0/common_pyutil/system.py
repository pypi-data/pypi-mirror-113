import os
import sys
import importlib.machinery
import importlib.util
from typing import List


def which(program):
    """
    This function is taken from
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def load_user_module(modname: str, search_path: List[str] = None):
    """`search_paths` is a list of paths. Defaults to `sys.path`"""
    if search_path is not None:
        spec = importlib.machinery.PathFinder.find_spec(modname, search_path)
    else:
        if modname.endswith(".py"):
            modname = modname[:-3]
        spec = importlib.machinery.PathFinder.find_spec(modname)
    if spec is None:
        print(f"Could not find module {modname}")
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod
