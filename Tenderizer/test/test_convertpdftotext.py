from logging import debug
import logging
from app_tk_widgets import ConvertPdfToText
from app_tk_widgets.utilities.pdftotext import OpenPDFError
from tkintertestcase import TKinterTestCase
from pdftotexttestcase import PDFToTextTestCase
import tkinter as tk
import shutil
from pathlib import Path




class TestRegexEntry(TKinterTestCase,PDFToTextTestCase):
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
    def setUp(self):
        super().setUp()
        self.new_tmp_dir()

    def tearDown(self):
        super().tearDown()
        self.remove_test_tmp_dir()
    
    def new_convertpdftotext(self):
        self.root.dataset=[]
        self.convertpdftotext=ConvertPdfToText(self.root)
        self.convertpdftotext.input.entry.insert(tk.END,self.input_dir.resolve())
        self.convertpdftotext.input.assert_dir()
        self.convertpdftotext.output.entry.insert(tk.END,self.output_dir.resolve())
        self.convertpdftotext.output.assert_dir()        
        self.pump_events()
        return self.convertpdftotext
    
    def test_convert_pdfs(self):
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
        self.assertNotIn(False,[i.converted for i in covnert_pdftotext.dataset])

    def test_delete_selection(self):
        covnert_pdftotext=self.new_convertpdftotext()
        covnert_pdftotext.import_pdfs()
        self.pump_events()
        self.assertEqual([i.name for i in covnert_pdftotext.dataset],self.pdfs)
        del_pdf=covnert_pdftotext.dataset[0]
        covnert_pdftotext.treeview.tree.selection_set(del_pdf.id)
        self.pump_events()
        covnert_pdftotext.treeview.delete_selection()
        self.assertNotIn(del_pdf.id,[i.id for i in covnert_pdftotext.dataset])

    def test_except_halts_conversion__then_log_and_raise(self):
        covnert_pdftotext=self.new_convertpdftotext()
        covnert_pdftotext.import_pdfs()
        self.pump_events()
        self.assertEqual([i.name for i in covnert_pdftotext.dataset],self.pdfs)
        del_pdf=Path(covnert_pdftotext.dataset[0].input_path)
        
        with self.assertLogs('app_tk_widgets.frames.convertpdftotext',level=logging.ERROR) as cm:
            del_pdf.unlink()
            with self.assertRaises(OpenPDFError):
                covnert_pdftotext.convert_paths()
            self.assertEqual(cm.output,[f'ERROR:app_tk_widgets.frames.convertpdftotext:Error opening a PDF file: "{del_pdf.resolve()}"'])
        self.pump_events()
        self.assertNotIn(True,[i.converted for i in covnert_pdftotext.dataset])



        