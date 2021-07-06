import unittest
from pathlib import Path
from os import chdir
import coverage

if __name__ == '__main__':
    cov=coverage.Coverage()
    cov.start()

    working_dir=Path(__file__).resolve().parent
    chdir(working_dir)
    
    loader = unittest.TestLoader()
    start_dir = './test'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)

    cov.stop()
    cov.save()

    cov.html_report()