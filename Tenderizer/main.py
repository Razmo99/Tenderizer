from version import __version__
import json
import logging
import logging.handlers
import os
import pathlib
import re
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
from io import StringIO
from pathlib import Path, PurePath
from re import M
from tkinter.constants import ANCHOR
from typing import Text

import app_tk_widgets
from dotenv import load_dotenv
from logger_colors import CustomFormatter

logger = logging.getLogger(__name__)
# ! TODO Dark Mode
# ! TODO Output Dir CSV Transaction Log


class AppMenu(tk.Menu):
    """ App menu bar """

    def __init__(self, master):
        tk.Menu.__init__(self, master)

        self.m_exit = tk.Menu(self, tearoff=False)
        self.m_exit.add_command(label='Exit', command=self.master.quit)
        self.add_cascade(menu=self.m_exit, label='Tenderizer')

        self.m_utils = tk.Menu(self, tearoff=False)
        self.m_utils.add_command(label='Regex Tester',
                                 command=self.open_regex_tester)
        self.add_cascade(menu=self.m_utils, label='Utilities')

        self.master.configure(menu=self)

    def open_regex_tester(master):
        x = tk.Toplevel(master)
        x.title('Regex Tester')
        regex_tester = app_tk_widgets.components.RegexTester(x)


class App(ttk.Notebook):
    """ Adds the main frames of tenderizer into a notebook """

    def __init__(self, master):
        ttk.Notebook.__init__(self, master)
        self.grid(sticky='nsew', padx=5, pady=5, ipady=5, ipadx=5)

        # Contains all Pdf information
        self.dataset = []

        self.pdf_to_text = app_tk_widgets.frames.ConvertPdfToText(self)
        self.pdf_Renamer = app_tk_widgets.frames.RegexMatcher(self)

        self.add(self.pdf_to_text, text='Pdf to Txt')
        self.add(self.pdf_Renamer, text='Regex Match')


def main():
    # target=Path(os.getenv("TARGET",None))
    # destination=Path(os.getenv("DESTINATION",None))
    # pdftotext_exe=Path(os.getenv("PDFTOTEXT",None))
    root = tk.Tk()
    s = ttk.Style()

    if root.getvar('tk_patchLevel') == '8.6.9' and os.name == 'nt':
        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.
            #
            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [elm for elm in s.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
        s.map('Treeview', foreground=fixed_map('foreground'),
              background=fixed_map('background'))

    app = App(root)
    menu = AppMenu(root)

    root.title('Tenderizer')
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.option_add('*tearOff', tk.FALSE)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()


if __name__ == "__main__":
    load_dotenv()
    if getattr(sys, 'frozen', False):
        # Change the current working directory to be the parent of main.py
        working_dir = pathlib.Path(sys._MEIPASS)
        os.chdir(working_dir)
    else:
        # Change the current working directory to be the parent of main.py
        working_dir = pathlib.Path(__file__).resolve().parent
        os.chdir(working_dir)
    if os.getenv('DEBUG', '').lower() == "true":
        LoggingLevel = logging.DEBUG
    else:
        LoggingLevel = logging.INFO
    # Initialise logging
    log_name = os.getenv("LOG_SAVE_LOCATION", 'tenderizer.log')
    logging_format = '%(asctime)s - %(levelname)s - [%(module)s]::%(funcName)s() - %(message)s'
    rfh = logging.handlers.RotatingFileHandler(
        filename=log_name,
        mode='a',
        maxBytes=5*1024*1024,
        backupCount=2,
        encoding='utf-8',
        delay=0
    )
    rfh.setFormatter(CustomFormatter)
    console = logging.StreamHandler()
    console.setLevel(LoggingLevel)
    console.setFormatter(CustomFormatter)
    logging.basicConfig(
        level=LoggingLevel,
        format=logging_format,
        handlers=[rfh, console]
    )
    logger.info(f'Working Dir: {str(working_dir)}')
    logger.info(
        f'Logging Level: {logging.getLevelName(logger.getEffectiveLevel())}')
    logger.info(f'Tenderizer version: {__version__}')
    main()
