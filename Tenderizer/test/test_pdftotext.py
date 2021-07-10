from pathlib import Path
from typing import Text
from app_tk_widgets import PDFToText
from app_tk_widgets.utilities.pdftotext import OpenPDFError,OpenOutputFileError
from pdftotexttestcase import PDFToTextTestCase
import unittest
class TestFileNamer(unittest.TestCase,PDFToTextTestCase):

    """
    Goals of this class

    * Convert a PDF to text
    * mkdir that are missing in the output folder
    * Raise exceptions from the pdftotext.exe
    * Log results of conversion

    Produced information
    * none

    Dependancies
    * Xpdf Tools > PDFToText

    """

    def setUp(self):
        self.new_tmp_dir()
        self.copy_pdf()
        self.pdftotext=PDFToText(self.pdftotext_exe)

    def tearDown(self):
        self.remove_test_tmp_dir()

    def test_convert_pdf_to_text(self):
        txt=self.output_dir / 'SB.3.txt'
        pdf=self.input_dir / 'SB.3.pdf'
        self.pdftotext.execute(
            pdf,
            txt)
        self.assertEqual(txt.is_file(),True)
        with txt.open('r') as data:
            self.assertIn('Drawing',data.read())

    def test_raise_open_pdf_error(self):
        pdf=self.input_dir / 'SB3.pdf'
        with self.assertRaises(OpenPDFError):
            result = self.pdftotext.execute(pdf)
    
    def test_output_none_convert_same_dir(self):
        txt=self.input_dir / 'SB.3.txt'
        pdf=self.input_dir / 'SB.3.pdf'
        self.pdftotext.execute(pdf)
        self.assertEqual(txt.is_file(),True)
        with txt.open('r') as data:
            self.assertIn('Drawing',data.read())

    def test_make_output_dir(self):
        txt=self.output_dir / 'testing\SB.3.txt'
        pdf=self.input_dir / 'SB.3.pdf'
        self.pdftotext.execute(pdf,txt)
        self.assertEqual(txt.is_file(),True)
        with txt.open('r') as data:
            self.assertIn('Drawing',data.read())        