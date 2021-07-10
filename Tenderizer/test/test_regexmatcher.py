import re
import logging
from app_tk_widgets import RegexMatcher, ConvertPdfToText
from tkintertestcase import TKinterTestCase
from pdftotexttestcase import PDFToTextTestCase
import tkinter as tk
import shutil
from pathlib import Path
import copy




class TestRegexEntry(TKinterTestCase,PDFToTextTestCase):
    """
    Goals of this class

    * Accept a user defined regular expression
    * Display pdfs new name based on current settings etc
    * Rename PDFs based on RE match(s)
     * Order can be specififed
    * Tag row Yellow when dir len is > 256
    * Tag row red when dir len is > 1024

    Produced information
     * New File Names
     * Match order
     * re matches for each pdf

    Operations
    * Rename the pdfs to the new file names produced

    Dependancies
    * Treeview
    * RegexMatchOrder
    * RegexEntry
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
        self.convertpdftotext.import_pdfs()
        self.pump_events()
        self.convertpdftotext.convert_paths()
        self.pump_events()
        self.masterdataset=copy.deepcopy(self.root.dataset)
        return self.convertpdftotext

    def refresh_dataset(self):
        if not getattr(self,'convertpdftotext',''):
            self.new_convertpdftotext()
        return copy.deepcopy(self.masterdataset)

    def new_regexmatcher(self):
        self.regexmatcher=RegexMatcher(self.root)
        self.regexmatcher.regex_entry.var.set(r'Drawing Title(.*)Scale')
        self.regexmatcher.regex_entry.vars[1].set(8)
        self.regexmatcher.regex_entry.vars[2].set(16)
        self.pump_events()
        self.regexmatcher.regex_entry.recompile()
        self.pump_events()
        return self.regexmatcher

    def test_load_pdfs(self):
        convert_pdftotext=self.new_convertpdftotext()
        regex_matcher=self.new_regexmatcher()
        regex_matcher.set_pdfs_new_name()
        self.pump_events()
        treeview=list(regex_matcher.treeview.tree.get_children())
        self.assertEqual(treeview,[i.id for i in convert_pdftotext.dataset])

    def test_delete_selection(self):
            self.refresh_dataset()
            regex_matcher=self.new_regexmatcher()
            regex_matcher.set_pdfs_new_name()
            self.pump_events()
            self.assertEqual([i.name for i in regex_matcher.dataset],self.pdfs)
            del_pdf=regex_matcher.dataset[0]
            regex_matcher.treeview.tree.selection_set(del_pdf.id)
            self.pump_events()
            regex_matcher.treeview.delete_selection()
            self.assertNotIn(del_pdf.id,[i.id for i in regex_matcher.dataset])

    def test_new_file_name(self)        :
        self.refresh_dataset()
        regex_matcher=self.new_regexmatcher()
        regex_matcher.set_pdfs_new_name()
        self.pump_events()
        regex_matcher.match_group_selector.var.set('1')
        regex_matcher.match_group_selector.option_menu_var.set('Underscore')
        regex_matcher.match_group_selector.compare_user_input()
        self.pump_events()
        regex_matcher.set_pdfs_new_name()
        self.pump_events()
        results=["SB_3_The_Lazy_Dev_jumped_over_the_Python_and_fou_nd_bug's.pdf",
            'SB_4_Debugging_Newline.pdf',
            'SB_5_Testing_For_Tricks_Yes.pdf',
            'SB_6_Testing_PDFToText_For_Bugs_.pdf']
        self.assertEqual(results,[i.new_name for i in regex_matcher.dataset])

    def test_rename_files(self):
        self.refresh_dataset()
        regex_matcher=self.new_regexmatcher()
        regex_matcher.set_pdfs_new_name()
        self.pump_events()
        regex_matcher.match_group_selector.var.set('1')
        regex_matcher.match_group_selector.option_menu_var.set('Underscore')
        regex_matcher.match_group_selector.compare_user_input()
        self.pump_events()
        regex_matcher.set_pdfs_new_name()
        self.pump_events()
        results=["SB_3_The_Lazy_Dev_jumped_over_the_Python_and_fou_nd_bug's.pdf",
            'SB_4_Debugging_Newline.pdf',
            'SB_5_Testing_For_Tricks_Yes.pdf',
            'SB_6_Testing_PDFToText_For_Bugs_.pdf']
        self.assertEqual(results,[i.new_name for i in regex_matcher.dataset])
        regex_matcher.rename_pdfs()
        self.pump_events()
        renamed_pdfs=self.get_outptut_pdfs()
        for i in regex_matcher.dataset:
            self.assertIn(i.new_name,renamed_pdfs)
    
    def test_except_halts_conversion_then_log_and_raise(self):
            self.refresh_dataset()
            regex_matcher=self.new_regexmatcher()
            regex_matcher.set_pdfs_new_name()
            self.pump_events()
            regex_matcher.match_group_selector.var.set('1')
            regex_matcher.match_group_selector.option_menu_var.set('Underscore')
            regex_matcher.match_group_selector.compare_user_input()
            self.pump_events()
            regex_matcher.set_pdfs_new_name()
            self.pump_events()
            all_pdf_names=[i.name for i in regex_matcher.dataset]
            self.assertEqual(all_pdf_names,self.pdfs)
            del_pdf=Path(regex_matcher.dataset[0].input_path)
            
            with self.assertLogs('app_tk_widgets.frames.regexmatcher',level=logging.ERROR) as cm:
                del_pdf.unlink()
                with self.assertRaises(OSError):
                    regex_matcher.rename_pdfs()
                    self.assertRegexpMatches(cm.output,re.compile(r'\[WinError 2\] The system cannot find the file specified:',flags=re.M|re.S))
            all_rename_ops=[i.rename_op for i in regex_matcher.dataset]
            self.assertIn((),all_rename_ops)
            all_pdfs_minus_del_pdf=[i.name for i in regex_matcher.dataset if not i.name == del_pdf.name]
            self.assertEqual(self.get_outptut_pdfs(),all_pdfs_minus_del_pdf)