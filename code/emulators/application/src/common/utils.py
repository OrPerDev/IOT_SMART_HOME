import os
import sys


def absolute_path(relative_path: str) -> str:
    root_dir = sys.modules["__main__"].__file__
    return os.path.join(os.path.dirname(str(root_dir)), relative_path)
