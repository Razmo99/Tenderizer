import os, pathlib, sys
from re import M
from pathlib import Path, PurePath
import logging
import logging.handlers
from tkinter.constants import ANCHOR
from typing import Text
from dotenv import load_dotenv
from pdf_utils import scan_tree, execute_pdftotext
from dataclasses import dataclass
import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk
import app_tk_widgets
from io import StringIO
import re
import json
logger = logging.getLogger(__name__)
# ! TODO Dark Mode
# ! TODO Output Dir CSV Transaction Log

@dataclass
class Pdf():
    """Class for Keeping track of all Pdf's being renamed"""
    name: str
    input_path: PurePath
    relative_output_path: PurePath
    output_path: PurePath
    converted: bool
    id: str
    text_data: str
    renamer_id: str
    regex_matches: re.Match
    regex_match_group: int
    new_name: str
    rename_op: tuple

    def __init__(self,id,name,input_path):
        self.id=id
        self.name=name
        self.input_path=input_path
        self.converted=False

    def __repr__(self):
        return self.name

class AppMenu(tk.Menu):

    def __init__(self, master):
        tk.Menu.__init__(self,master)
        

        self.m_exit = tk.Menu(self,tearoff=False)
        self.m_exit.add_command(label='Exit',command=self.master.quit)
        self.add_cascade(menu=self.m_exit,label='Tenderizer')
        
        self.m_utils = tk.Menu(self,tearoff=False)
        self.m_utils.add_command(label='Regex Tester',command=self.open_regex_tester)
        self.add_cascade(menu=self.m_utils,label='Utilities')

        self.master.configure(menu=self)
    
    def open_regex_tester(master):
        x=tk.Toplevel(master)
        x.title('Regex Tester')
        regex_tester = app_tk_widgets.components.RegexTester(x)

class RegexMatcher(ttk.Frame):

    def __init__(self,master):

        ttk.Frame.__init__(self,master)
        self.dataset=self.master.dataset

        self.grid(row=0,column=0,sticky='nsew')
        self.grid_rowconfigure(0,weight=3)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        self.regex_entry = app_tk_widgets.components.RegexEntry(self)
        self.regex_entry.grid(row=0,column=0)

        # Method to generate a new pdf file name based on the selections in the RegexMatchOrder on screen
        self.new_match_ordered_name=self.regex_entry.match_group_selector.new_file_name
        # Method to update the tree view in the RegexMatchOrder on screen
        self.new_match_order_examples=self.regex_entry.match_group_selector.add_tree_view_items

        self.treeview = app_tk_widgets.components.TreeView(self,'Match View',('Name','New Name'))
        self.treeview.grid(row=1,column=0)
        
        self.treeview.load_button.configure(command=self.load_dataset,state='normal')
        self.treeview.convert_button.configure(command=self.convert_pdfs,state='normal',text='rename')

        self.treeview.convert_button.configure(command=self.convert_pdfs,state='normal',text='Rename')

        self.treeview.right_click_selection_menu.add_command(label='Regex Utility',command=lambda :self.open_regex_util())

    def load_dataset(self):
        dataset=self.dataset
        if dataset:
            # Clear out the treeview
            self.treeview.tree.delete(*self.treeview.tree.get_children())
            for pdf in dataset:
                tv_new_name=self.search_re_expression(pdf)
                self.treeview.tree.insert('','end',iid=pdf.id,values=[pdf.name,tv_new_name])
            if dataset[1].converted and dataset[1].regex_matches:
                self.new_match_order_examples(dataset[1].regex_matches)
    
    def confirm_re_compiled(self):
        """ Checks that the re is compiled and no syntax warnings are present"""
        re_compiled = self.regex_entry.compiled
        re_compiled_status = self.regex_entry.statusdisplay.cget('text')
        if  re_compiled_status == "" and re_compiled:
            return re_compiled
    
    def search_re_expression(self, pdf):
        if pdf.converted:
            # Check if the regex entry is valid and compiled
            compiled_re=self.confirm_re_compiled()
            if  compiled_re:
                re_matches=compiled_re.search(pdf.text_data)
                if not re_matches is None:
                    # Update the dataset
                    pdf.regex_matches=re_matches
                    # Construct the new file name
                    suffix=pdf.input_path.suffix
                    prefix=pdf.name.replace(suffix,'')
                    new_name = self.new_match_ordered_name(prefix,suffix,re_matches)
                    if new_name:
                        pdf.new_name=new_name
                        return new_name

    def convert_pdfs(self):
        # Grab the Data that has all pdf path info
        dataset=self.dataset
        if dataset:
            # Iterate over the data set
            for pdf in dataset:
                input_path=Path(pdf.input_path)
                rename_path=input_path.parent / pdf.new_name
                output={
                    'operation': 'rename',
                    'input_path': f'{input_path.resolve()}',
                    'rename_path': f'{rename_path.resolve()}',
                    'completed': True
                }
                try:
                    pdf.rename_op=(input_path,rename_path)
                    input_path.rename(rename_path)
                except:
                    output['completed']=False
                    logging.exception(json.dumps(output))
                    raise
                else:
                    logging.info(json.dumps(output))
    
    def open_regex_util(self):
        x=tk.Toplevel(self.master)
        x.title('Regex Tester')
        selection = self.treeview.tree.selection()
        text_data=''
        for pdf in self.dataset:
            if pdf.id == selection[0]:
                text_data=pdf.text_data

        self.regex_tester = app_tk_widgets.components.RegexTester(x)
        self.regex_tester.regexdisplay.delete(0,tk.END)
        self.regex_tester.regexdisplay.insert(0,self.regex_entry.var.get())
        self.regex_tester.stringdisplay.delete(1.0,tk.END)
        self.regex_tester.stringdisplay.insert(1.0,text_data)

        self.regex_tester.recompile()

class ConvertPdfToText(ttk.Frame):


    def __init__(self, master):
        # Init the main Frame
        ttk.Frame.__init__(self,master)
        self.grid(row=0,column=0,sticky='nsew')
        self.grid_rowconfigure(2,weight=1)
        self.grid_columnconfigure(0,weight=1)    
        # Input directory or file to convert
        self.input = app_tk_widgets.components.BrowseDir(self,'Input Path')
        self.input.error_msg.trace_add(('write'),self.callback_treeview_load_button)
        self.input.grid(row=0,column=0)
        # Output directory to store converted txt files
        self.output = app_tk_widgets.components.BrowseDir(self,'Output Path')
        self.output.error_msg.trace_add(('write'),self.callback_treeview_convert_button)
        self.output.grid(row=1,column=0)
        # Tree view to display the loaded PDF's
        self.treeview = app_tk_widgets.components.TreeView(self,'PDF View',('Name','Input Path','Output Path',))
        self.treeview.grid(row=2,column=0)
        # Configure the buttons in the treeview class
        self.treeview.load_button.configure(command=self.load_pdfs)
        self.treeview.convert_button.configure(command=self.convert_paths)
        # Holds information about converted PDF's
        self.dataset=self.master.dataset
        
        #TODO ! Remove these after testing
        self.input.dir.set("C:\Projects\PDFs\Animals")
        self.input.assert_dir()
        self.output.dir.set("C:\Projects\Output")
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
            x=execute_pdftotext(
                exe=Path('xpdf/pdftotext.exe'),
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

    def load_pdfs(self):
        """ Load pdf path information from the specified directory """        
        # Clear contents of the tree view
        self.treeview.tree.delete(*self.treeview.tree.get_children())
        # Empty the data set
        del self.dataset[:]
        # Get the input directory as a path
        p=Path(self.input.dir.get())
        # Get the input directory as a Pure Path
        # Doing this to make use of the relative_to method
        pp=PurePath(self.input.dir.get())
        # Output Path
        op=PurePath(self.output.dir.get())
        for scan in scan_tree(p):
            # scan pure path Directory Object
            scan_pure_path=PurePath(scan)
            # Directory object relative to the input directoy
            scan_pure_path_rel=scan_pure_path.relative_to(self.input.dir.get())
            # Output Path + relative scan path
            final_output_path=op.joinpath(scan_pure_path_rel)
            # Final output path plus the file name
            final_path = final_output_path.parent.joinpath(final_output_path.name.replace('.pdf','.txt'))
            # Check if its a Pdf
            if scan_pure_path.suffix == '.pdf' :
                # Tree view values
                tv_values = [scan.name,scan.path,final_path]
                # Insert the tree view item
                tv_id = self.treeview.tree.insert('','end',values=tv_values)
                # Initial Pdf Data class object
                i = Pdf(
                    tv_id,
                    scan.name,
                    PurePath(scan.path)
                )
                # Add additional info to the object
                i.output_path=PurePath(final_path)
                i.relative_output_path=PurePath(scan_pure_path_rel)
                self.dataset.append(i)

class App(ttk.Notebook):

    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.grid(sticky='nsew',padx=5,pady=5,ipady=5,ipadx=5)
        
        # Contains all info on PDfs for the session
        self.dataset=[]

        self.pdf_to_text=ConvertPdfToText(self)
        self.pdf_Renamer = RegexMatcher(self)

        self.add(self.pdf_to_text,text='Pdf to Txt')
        self.add(self.pdf_Renamer,text='Regex Match')

def main():
    #target=Path(os.getenv("TARGET",None))
    #destination=Path(os.getenv("DESTINATION",None))
    #pdftotext_exe=Path(os.getenv("PDFTOTEXT",None))
    root = tk.Tk()
    app = App(root)
    menu = AppMenu(root)
    root.title('Tenderizer')
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.option_add('*tearOff', tk.FALSE)
    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)
    root.mainloop()
    
if __name__ == "__main__":
    load_dotenv()
    if getattr(sys,'frozen',False):
        #Change the current working directory to be the parent of the main.py
        working_dir=pathlib.Path(sys._MEIPASS)
        os.chdir(working_dir)
    else:
        #Change the current working directory to be the parent of the main.py
        working_dir=pathlib.Path(__file__).resolve().parent
        os.chdir(working_dir)
    if os.getenv('DEBUG','').lower() == "true":
        LoggingLevel=logging.DEBUG
    else:
        LoggingLevel=logging.INFO
    #Initialise logging
    log_name = os.getenv("LOG_SAVE_LOCATION",'tenderizer.log')
    logging_format='%(asctime)s - %(levelname)s - [%(module)s]::%(funcName)s() - %(message)s'
    rfh = logging.handlers.RotatingFileHandler(
    filename=log_name, 
    mode='a',
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding='utf-8',
    delay=0
    )
    console=logging.StreamHandler()
    console.setLevel(LoggingLevel)
    logging.basicConfig(
        level=LoggingLevel,
        format=logging_format,
        handlers=[rfh,console]
    )
    logger.info('Working Dir: '+str(working_dir))
    logger.info('Logging Level: '+str(LoggingLevel))
    main()