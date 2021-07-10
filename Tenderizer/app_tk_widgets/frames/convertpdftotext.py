import tkinter as tk
import tkinter.ttk as ttk
import logging
import json
import os
from pathlib import Path, PurePath
from ..components import RegexEntry, TreeView, RegexMatchOrder,RegexTester, BrowseDir
from .. utilities import Pdf, PDFToText
from .. utilities.pdftotext import OpenOutputFileError, PDFPermissionsError, OpenPDFError

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
        self.load_btn=self.treeview.load_button
        self.convert_btn=self.treeview.convert_button
        self.load_btn.configure(command=self.import_pdfs)
        self.convert_btn.configure(command=self.convert_paths)
        # Holds information about converted PDF's
        self.dataset=self.master.dataset
        
        self.pdftotext=PDFToText(Path('xpdf/pdftotext.exe'))
    
    def disable_tv_btns(self):
        self.load_btn.configure(state=tk.DISABLED)
        self.convert_btn.configure(state=tk.DISABLED)

    def enable_tv_btns(self):
        self.load_btn.configure(state=tk.NORMAL)
        self.convert_btn.configure(state=tk.NORMAL)

    def get_load_state(self) -> str:
        state=self.load_btn.cget('state')
        return state
    
    def get_convert_state(self) -> str:
        return self.convert_btn.cget('state')

    def callback_treeview_convert_button(self,var,indx,mode):
        """ Controls the state of the Output button in the treeview based on if the input path is valid """
        err=self.output.error_msg.get()
        if not err:
            self.convert_btn.configure(state=tk.NORMAL)
        else:
            self.convert_btn.configure(state=tk.DISABLED)
    
    def callback_treeview_load_button(self,var,indx,mode):
        """ Controls the state of the load button in the treeview based on if the input path is valid """
        err=self.input.error_msg.get()
        if not err:
            self.load_btn.configure(state=tk.NORMAL)
        else:
            self.load_btn.configure(state=tk.DISABLED)
    
    def convert_paths(self,iter_obj=None) -> None:
        """Convert PDF's to text"""
        if not iter_obj:
            iter_obj=iter(self.dataset)
            self.disable_tv_btns()
        try:
            pdf=next(iter_obj)
        except StopIteration:
            self.enable_tv_btns()
            return
        else:
            exit_code = self.convert_path(pdf)
            if exit_code == 0:
                self.read_pdf_text(pdf)
                self.treeview.tree.item(pdf.id,tags=('green'))
                self.treeview.tree.see(pdf.id)
            else:
                pdf.converted=False
                self.treeview.tree.item(pdf.id,tags=('red'))
            self.after_idle(self.convert_paths,iter_obj)

    def convert_path(self, pdf):
        try:
            result = self.pdftotext.execute(
                    input_path=Path(pdf.input_path),
                    output=Path(pdf.output_path)
                )
        except Exception as e:
            tk.messagebox.showerror("Unhandled Exception", e.__str__())
            logging.exception(e)
            raise
        else:
            return result
  
    def read_pdf_text(self, pdf: Pdf) -> None:
        """ Read generated txt from pdf doc add it to pdf object"""
        with Path(pdf.output_path).open('r') as p:
            txt=p.read()
            pdf.text_data=txt
        pdf.converted=True

    def scan_tree(self,path):
        """Recursively yield DirEntry objects for given directory."""
        with os.scandir(path) as scan:
            for entry in scan:
                if entry.is_dir(follow_symlinks=False):
                    yield from self.scan_tree(entry.path)
                else:
                    yield entry    
    
    def new_pdf(self,dir_entry: os.DirEntry,input_dir:PurePath,output_dir:PurePath) -> Pdf:
        """ import pdf from path """
        scan_path=PurePath(dir_entry)
        if dir_entry.is_file and scan_path.suffix == '.pdf':
            pdf=Pdf(scan_path)
            pdf.input_dir=PurePath(input_dir)
            pdf.output_dir=output_dir
            pdf.set_output_path()
            return pdf

    def import_pdfs(self) -> None:
        """ Load pdf path information from the specified directory """
        self.treeview.tree.delete(*self.treeview.tree.get_children())
        del self.dataset[:]
        input_dir=Path(self.input.dir.get())
        output_dir=PurePath(self.output.dir.get())
        for dir_entry in self.scan_tree(input_dir):
            pdf=self.new_pdf(dir_entry,PurePath(input_dir),output_dir)
            if pdf:
                self.dataset.append(pdf)
                tv_values = [pdf.name,pdf.input_path,pdf.output_path]
                tv_id = self.treeview.tree.insert('','end',values=tv_values)
                pdf.id=tv_id
