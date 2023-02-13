import pathlib
import PyInstaller.__main__
import os

if __name__ == '__main__':
    working_dir = pathlib.Path(__file__).resolve().parent
    os.chdir(working_dir)
    PyInstaller.__main__.run([
        'main.py',
        '--onedir',
        '--windowed',
        '--name',
        'Tenderizer',
        '--version-file',
        'version.rc'
    ])