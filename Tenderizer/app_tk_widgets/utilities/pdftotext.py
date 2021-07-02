import os
from pathlib import Path
from subprocess import Popen
import logging
import json
logger = logging.getLogger(__name__)

class PDFToText(object):
    
    def __init__(self,exe):
        self.exe = exe

    def execute(self,input_path,output=None):
        """ Calls xpdf pdftotext as a subprocess"""
        args=[f'{self.exe.resolve()}','','']
        if input_path.is_file():
            logger.debug('Converting a file')
            already_existed=False
            created_dir_structure=False
            args[1]=f'{input_path}'
            # Handles if the output is a directory or file
            if output:
                if not output.parent.exists():
                    created_dir_structure=True
                    output.parent.mkdir(parents=True,exist_ok=True)
                if output.exists():
                    already_existed=True
                if output.suffix =='.pdf':
                    args[2]=f'{output.resolve()}'.replace('.pdf','.txt')
                elif output.suffix == '.txt':
                    args[2]=f'{output.resolve()}'
            pdftotext=Popen(
                args
            )
            pdftotext.wait()
            if not pdftotext.returncode == 0:
                logger.debug(pdftotext.returncode)
            else:
                dump={
                    'input_path': f'{input_path.resolve()}',
                    'output_path': f'{output.resolve()}',
                    'already_existed': already_existed,
                    'created_dir_structure': created_dir_structure if not created_dir_structure else f'{output.parent}',
                    'return_code' : pdftotext.returncode
                }
                logging.info(
                    json.dumps(dump)
                )
            return pdftotext.returncode