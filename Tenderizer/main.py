import os, pathlib, sys
from pathlib import Path, PurePath
import logging
import logging.handlers
from dotenv import load_dotenv
from pdf_utils import scan_tree, execute_pdftotext
from dataclasses import dataclass
import tkinter.filedialog
import tkinter as tk
import tkinter.ttk as ttk
import app_tk_widgets
from regex_tester import RegexTester
from io import StringIO
logger = logging.getLogger(__name__)

@dataclass
class Pdf():
    """Class for Keeping track of all Pdf's being renamed"""
    name: str
    input_path: Path
    relative_output_path: Path
    output_path: Path
    converted: bool
    id: str
    text_data: StringIO

    def __init__(self,id,name,input_path):
        self.id=id
        self.name=name
        self.input_path=input_path

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
        regex_tester = RegexTester(x)



class PdfRenamer(ttk.Frame):

    def __init__(self,master):
        ttk.Frame.__init__(self,master)
        self.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)

        regex_entry = app_tk_widgets.components.RegexEntry(self)



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
        self.treeview = app_tk_widgets.components.TreeView(self,'PDF View',('Name','Path','Relative'))
        self.treeview.grid(row=2,column=0)
        # Holds information about converted PDF's
        self.dataset=[]
        #TODO REmove these after testing
        self.input.dir.set("C:\Projects\PDFs\Animals")
        self.output.dir.set("C:\Projects\Output")
    
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
        op=PurePath(self.output.dir.get())
        for pdf in self.dataset:
            final_output_path=op.joinpath(pdf.relative_output_path)
            x=execute_pdftotext(
                exe=Path('pdftotext.exe'),
                p=Path(pdf.input_path),
                o=Path(final_output_path)
            )
            if x == 0:
                pdf.converted=True
            else:
                pdf.converted=False

    def load_pdfs(self):
        """ Load pdf path information from the specified directory """        

        self.treeview.tree.delete(*self.treeview.tree.get_children())
        self.dataset=[]
        p=Path(self.input.dir.get())
        pp=PurePath(self.input.dir.get())
        self.dataset=[]
        for scan in scan_tree(p):
            spp=PurePath(scan)
            spp_rel=spp.relative_to(self.input.dir.get())
            if spp.suffix == '.pdf' :
                x = self.treeview.tree.insert('','end',values=(scan.name,scan.path,spp_rel))
                i = Pdf(
                    x,
                    scan.name,
                    scan.path
                )
                i.relative_output_path=spp_rel
                self.dataset.append(i)

class App(ttk.Notebook):

    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.grid(sticky='nsew',padx=5,pady=5,ipady=5,ipadx=5)

        pdf_to_text=ConvertPdfToText(self)
        pdf_Renamer = PdfRenamer(self)
        self.add(pdf_to_text,text='Pdf to Txt')
        self.add(pdf_Renamer,text='Pdf Renamer')
        

def main():
    target=Path(os.getenv("TARGET",None))
    destination=Path(os.getenv("DESTINATION",None))
    pdftotext_exe=Path(os.getenv("PDFTOTEXT",None))
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
    if os.getenv('DEBUG').lower() == "true":
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