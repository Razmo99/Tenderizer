import os
from pathlib import Path
from subprocess import Popen
import logging
logger = logging.getLogger(__name__)


def execute_pdftotext(exe,p,o=None):
    """ Calls xpdf pdftotext as a subprocess"""
    # Only accept a path Object
    if not isinstance(exe,Path):
        raise TypeError("exe: Expecting PathLib.Path")
    if not isinstance(p,Path):
        raise TypeError("p: Expecting PathLib.Path")
    if not isinstance(o,Path):
        raise TypeError("o: Expecting PathLib.Path")                
    args=[f'{exe.resolve()}','','']
    # Handles Individual file
    if p.is_file():
        logger.debug('Converting a file')
        args[1]=f'{p}'
        # Handles if the output is a directory or file
        if o:
            if not o.parent.exists():
                logger.debug(f'{o.parent} Creating Directory Stucture')
                o.parent.mkdir(parents=True,exist_ok=True)
            if o.exists():
                logging.info(f'{o.resolve()} already Exists')
            if o.suffix =='.pdf':
                args[2]=f'{o.resolve()}'.replace('.pdf','.txt')
        pdftotext=Popen(
            args
        )
        pdftotext.wait()
        if not pdftotext.returncode == 0:
            logger.debug(pdftotext.returncode)
        return pdftotext.returncode
    # Handles in the input is a directory
    elif p.is_dir():
        logger.debug('Converting a directory')
        # Handles if the output directory was not provided
        if not o.is_dir():
            logger.warning('Ouput is not a directory')
            o=Path(f'{p.parent}\\{p.name}_txt')
            if not o.exists():
                logger.debug('Creating directory: '+o.name)
                o.mkdir()
        elif not o.exists():
            logger.warning(f'Creating dir {o}')
            o.mkdir()
        pdf_files=p.rglob(f'*.pdf')
        for index,pdf_file in enumerate(pdf_files,start=1):
            args[1]=f'{pdf_file}'
            args[2]=f"{o}\\{pdf_file.name.replace('.pdf','.txt')}"
            pdftotext=Popen(
                args
            )
            pdftotext.wait()
            if not pdftotext.returncode == 0:
                logger.warning(f'pdftotext returned: {pdftotext.returncode}')
        logger.debug(f'Processed {index} files')
        

def scan_tree(path):
    """Recursively yield DirEntry objects for given directory."""
    with os.scandir(path) as scan:
        for entry in scan:
            if entry.is_dir(follow_symlinks=False):
                yield from scan_tree(entry.path)
            else:
                yield entry    