import shutil
import os
import stat
from pathlib import Path

from main_interface import MainInterface, interface_loop


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_cache(input_path):
    for path in input_path.iterdir():
        if path.is_dir() and path.name == '__pycache__':
            shutil.rmtree(path, onerror=remove_readonly)
        elif path.is_dir():
            delete_cache(path)


def main():
    try:
        interface = MainInterface()
        interface_loop(interface)
        delete_cache(Path(__file__).parent.parent)
    except Exception as e:
        delete_cache(Path(__file__).parent.parent)
        raise e


if __name__ == '__main__':
    main()
