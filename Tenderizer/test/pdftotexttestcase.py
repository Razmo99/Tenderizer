from abc import ABC
from pathlib import Path
import shutil
class PDFToTextTestCase():

    def new_tmp_dir(self):
        """ Make """
        self.pdfs=[]
        self.test_dir=Path('.\\test_tmp')
        self.input_dir=Path('.\\test_tmp\input')
        self.input_dir.mkdir(exist_ok=True,parents=True)
        self.pdftotext_exe=Path('.\\xpdf\pdftotext.exe')
        
        self.output_dir=Path('.\\test_tmp\outptut')
        self.output_dir.mkdir(exist_ok=True,parents=True)
        self.copy_pdf()

    def get_outptut_pdfs(self):
        return [i.name for i in self.input_dir.glob('*.pdf')]

    def copy_pdf(self):
        self.test_pdfs=Path('.\\test_pdfs')
        for src_file in self.test_pdfs.glob('*.pdf'):
            self.pdfs.append(src_file.name)
            shutil.copy(src_file,self.input_dir)
    
    def remove_test_tmp_dir(self):
        shutil.rmtree(self.test_dir)
