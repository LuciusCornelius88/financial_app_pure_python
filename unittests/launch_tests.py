import unittest
import shutil
import os, stat, sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'sources_tests'))
sys.path.append(str(Path(__file__).parent / 'transactions_tests'))

from test_source_model import TestSource


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
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSource)
        unittest.TextTestRunner().run(test_suite)
        delete_cache(Path(__file__).parent.parent)
    except Exception as e:
        print(e)
        delete_cache(Path(__file__).parent.parent)


if __name__ == '__main__':
    main()
        

