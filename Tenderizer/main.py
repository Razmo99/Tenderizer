import os, pathlib, sys
from re import M
from pathlib import Path, PurePath
import logging
import logging.handlers
from tkinter.constants import ANCHOR
from typing import Text
from dotenv import load_dotenv
from pdf_utils import scan_tree, execute_pdftotext
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

class App(ttk.Notebook):

    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.grid(sticky='nsew',padx=5,pady=5,ipady=5,ipadx=5)
        
        # Contains all info on PDfs for the session
        self.dataset=[]

        self.pdf_to_text=app_tk_widgets.frames.ConvertPdfToText(self)
        self.pdf_Renamer = app_tk_widgets.frames.RegexMatcher(self)

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