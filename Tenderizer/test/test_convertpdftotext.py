from app_tk_widgets import ConvertPdfToText
from tkintertestcase import TKinterTestCase
import re
import tkinter as tk
import unittest
import os
import shutil
from pathlib import Path, PurePath




class TestRegexEntry(TKinterTestCase):
    """
    Goals of this class

    * Specify a input and output dir to process PDF's
    * Load PDF's and view PDF's in a dir
    * Convert PDF's to text
    * remove specific PDF's from being processed

    Produced information
    * Populates the dataset list with pdfs
     * input ouput info
     * raw text data

    Dependancies
    * Treeview
    * BrowseDir
    * PDFToText
    * Pdf

    """
    def new_convertpdftotext(self):
        self.root.dataset=[]
        self.convertpdftotext=ConvertPdfToText(self.root)
        self.convertpdftotext.input.entry.insert(tk.END,self.input_dir.resolve())
        self.convertpdftotext.input.assert_dir()
        self.convertpdftotext.output.entry.insert(tk.END,self.output_dir.resolve())
        self.convertpdftotext.output.assert_dir()        
        self.pump_events()
        return self.convertpdftotext

    def new_tmp_dir(self):
        """ Make """
        self.pdfs=[]
        self.test_dir=Path('.\\test_tmp')
        self.input_dir=Path('.\\test_tmp\input')
        self.input_dir.mkdir(exist_ok=True,parents=True)
        
        self.output_dir=Path('.\\test_tmp\outptut')
        self.output_dir.mkdir(exist_ok=True,parents=True)
        self.copy_pdf()
    
    def copy_pdf(self):
        self.test_pdfs=Path('.\\test_pdfs')
        for src_file in self.test_pdfs.glob('*.pdf'):
            self.pdfs.append(src_file.name)
            shutil.copy(src_file,self.input_dir)
    
    def remove_test_tmp_dir(self):
        shutil.rmtree(self.test_dir)
    
    def test_convert_pdfs(self):
        self.new_tmp_dir()
        covnert_pdftotext=self.new_convertpdftotext()
        
        self.assertEqual(covnert_pdftotext.get_load_state().string,tk.NORMAL)
        self.assertEqual(covnert_pdftotext.get_convert_state().string,tk.NORMAL)

        covnert_pdftotext.import_pdfs()
        self.pump_events()
        self.assertEqual([i.name for i in covnert_pdftotext.dataset],self.pdfs)
        covnert_pdftotext.convert_paths()
        self.pump_events()
        dataset_files=[i.output_path.name for i in covnert_pdftotext.dataset]
        output_files=[i.name for i in self.output_dir.iterdir()]
        self.assertEquals(dataset_files,output_files)
        self.remove_test_tmp_dir()

        