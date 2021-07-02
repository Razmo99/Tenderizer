import unittest
from pathlib import Path
from os import chdir

if __name__ == '__main__':
    working_dir=Path(__file__).resolve().parent
    chdir(working_dir)
    
    loader = unittest.TestLoader()
    start_dir = './test'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)