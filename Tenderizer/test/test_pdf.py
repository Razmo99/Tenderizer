from pathlib import PurePath
from app_tk_widgets import Pdf
import unittest
from pathlib import Path, PurePath

class TestPdf(unittest.TestCase):

    def setUp(self):
        self.pdf=Pdf(
            PurePath('C:\Projects\PDFS\SomePDF.pdf')
        )
        self.pdf.output_dir=PurePath('C:\Output')
        self.pdf.input_dir=PurePath('C:\Projects')

    def test_path_rel_input_dir(self):
        x=self.pdf.get_input_path_rel_dir()
        self.assertEqual(x,PurePath('PDFS/SomePDF.pdf'))

    def test_generate_output_path(self):
        self.pdf.set_output_path()
        self.assertEqual(self.pdf.output_path,PurePath('C:\Output\PDFS\SomePDF.txt'))


