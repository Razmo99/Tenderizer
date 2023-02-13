import json
import logging
import os
import subprocess
from pathlib import Path, PurePath
from subprocess import Popen

logger = logging.getLogger(__name__)


class PDFToText(object):

    def __init__(self, exe):
        self.exe = exe

    def execute(self, input_path, output=None):
        """ Calls xpdf pdftotext as a subprocess"""
        args = [f'{self.exe.resolve()}', '', '']
        already_existed = False
        created_dir_structure = False
        args[1] = f'{input_path.resolve()}'
        if output:
            if not output.parent.exists():
                created_dir_structure = True
                output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists():
                already_existed = True
            args[2] = PurePath(output.resolve()).with_suffix('.txt').__str__()
        if output is None:
            del args[2]
        pdftotext = Popen(
            args,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        pdftotext.wait()
        if not pdftotext.returncode == 0:
            if pdftotext.returncode == 1:
                raise OpenPDFError(args)
            elif pdftotext.returncode == 2:
                raise OpenOutputFileError(args)
            elif pdftotext.returncode == 3:
                raise PDFPermissionsError(args)
            elif pdftotext.returncode == 99:
                raise XPDFTools(args)
        else:
            dump = {
                'input_path': args[1],
                'output_path': args[2] if len(args) == 3 else PurePath(args[1]).with_suffix('.txt').__str__(),
                'already_existed': already_existed,
                'created_dir_structure': created_dir_structure if not created_dir_structure else f'{output.parent}',
                'return_code': pdftotext.returncode
            }
            logger.info(
                json.dumps(dump)
            )
        return pdftotext.returncode


class XPDFTools(Exception):
    """ Basic exception for errors raised by xpdf tools """

    def __init__(self, arguments, msg=None) -> None:
        self.msg = msg if msg else 'Error with Xpdf Tools'
        super(XPDFTools, self).__init__(self.msg)
        self.arguments = arguments


class OpenPDFError(XPDFTools):
    """Error opening the PDF File"""

    def __init__(self, arguments, msg=None):
        super(OpenPDFError, self).__init__(
            arguments,
            f'Error opening a PDF file: "{arguments[1]}"'
        )


class OpenOutputFileError(XPDFTools):
    """Error opening the PDF Output File"""

    def __init__(self, arguments, msg=None):
        super(OpenPDFError, self).__init__(
            arguments,
            f'Error opening a PDF Output file: "{arguments[2]}"'
        )


class PDFPermissionsError(XPDFTools):
    """ PDF Permission Error"""

    def __init__(self, arguments, msg=None):
        super(OpenPDFError, self).__init__(
            arguments,
            f'Error with PDF Permissions: "{arguments[1]}"'
        )
