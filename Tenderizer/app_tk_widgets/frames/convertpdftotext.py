import tkinter as tk
import tkinter.ttk as ttk
import logging
import json
import os
from pathlib import Path, PurePath
from ..components import RegexEntry, TreeView, RegexMatchOrder,RegexTester, BrowseDir
from .. utilities import Pdf, PDFToText

class ConvertPdfToText(ttk.Frame):


    def __init__(self, master):
        # Init the main Frame
        ttk.Frame.__init__(self,master)
        self.grid(row=0,column=0,sticky='nsew')
        self.grid_rowconfigure(2,weight=1)
        self.grid_columnconfigure(0,weight=1)    
        # Input directory or file to convert
        self.input = BrowseDir(self,'Input Path')
        self.input.error_msg.trace_add(('write'),self.callback_treeview_load_button)
        self.input.grid(row=0,column=0)
        # Output directory to store converted txt files
        self.output = BrowseDir(self,'Output Path')
        self.output.error_msg.trace_add(('write'),self.callback_treeview_convert_button)
        self.output.grid(row=1,column=0)
        # Tree view to display the loaded PDF's
        self.treeview = TreeView(self,'PDF View',('Name','Input Path','Output Path',))
        self.treeview.grid(row=2,column=0)
        # Configure the buttons in the treeview class
        self.treeview.load_button.configure(command=self.load_pdf_paths)
        self.treeview.convert_button.configure(command=self.convert_paths)
        # Holds information about converted PDF's
        self.dataset=self.master.dataset
        
        self.pdftotext=PDFToText(Path('xpdf/pdftotext.exe'))

        #TODO ! Remove these after testing
        self.input.dir.set("C:/Projects/o_elec_weird - Copy")
        self.input.assert_dir()
        self.output.dir.set("C:/Projects/o_Elec_draw_char")
        self.output.assert_dir()
    
    def callback_treeview_convert_button(self,var,indx,mode):
        """ Controls the state of the Output button in the treeview based on if the input path is valid """
        err=self.output.error_msg.get()
        if not err:
            self.treeview.convert_button.configure(state='normal')
        else:
            self.treeview.convert_button.configure(state='disabled')
    
    def callback_treeview_load_button(self,var,indx,mode):
        """ Controls the state of the load button in the treeview based on if the input path is valid """
        err=self.input.error_msg.get()
        if not err:
            self.treeview.load_button.configure(state='normal')
        else:
            self.treeview.load_button.configure(state='disabled')
    
    def convert_paths(self):
        """Convert PDF's to text"""
        for pdf in self.dataset:
            output_path=Path(pdf.output_path)
            x=self.pdftotext.execute(
                p=Path(pdf.input_path),
                o=output_path
            )
            if x == 0:
                try:
                    # read the text document and add it to the data set
                    with output_path.open('r') as p:
                        txt=p.read()
                        pdf.text_data=txt   
                except:
                    raise
                else:
                    pdf.converted=True
            else:
                logging.debug(f'Failed to convert: {pdf.input_path.resolve()}')
                pdf.converted=False

    def scan_tree(self,path):
        """Recursively yield DirEntry objects for given directory."""
        with os.scandir(path) as scan:
            for entry in scan:
                if entry.is_dir(follow_symlinks=False):
                    yield from self.scan_tree(entry.path)
                else:
                    yield entry    
    
    def load_pdf_paths(self):
        """ Load pdf path information from the specified directory """
        self.treeview.tree.delete(*self.treeview.tree.get_children())
        del self.dataset[:]
        input_dir=Path(self.input.dir.get())
        output_dir=PurePath(self.output.dir.get())
        for scan in self.scan_tree(input_dir):
            scan_path=PurePath(scan)
            scan_path_rel_input_dir=scan_path.relative_to(input_dir)
            scan_output_dir=output_dir.joinpath(scan_path_rel_input_dir)
            scan_output_path = scan_output_dir.parent.joinpath(scan_output_dir.name.replace('.pdf','.txt'))
            if scan_path.suffix == '.pdf' :
                tv_values = [scan.name,scan.path,scan_output_path]
                tv_id = self.treeview.tree.insert('','end',values=tv_values)
                pdf = Pdf(tv_id,scan.name,PurePath(scan.path))
                pdf.output_path=PurePath(scan_output_path)
                pdf.relative_output_path=PurePath(scan_path_rel_input_dir)
                self.dataset.append(pdf)
