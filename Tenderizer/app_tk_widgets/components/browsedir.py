from pathlib import Path
import logging
import logging.handlers
import tkinter.filedialog
import tkinter as tk
from tkinter.constants import CENTER
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)

class BrowseDir(ttk.LabelFrame):
    """ Class that created a frame widget that contains some elements to select or manually enter in a directory """
    def __init__(self, master,lf_title):
        self.title=lf_title
        ttk.LabelFrame.__init__(self,master,text=self.title)
        self.dir = tk.StringVar(master,name=f'{self.title}_dir')
        self.error_msg = tk.StringVar(master,name=f'{self.title}_error_msg')
        self.error_msg.set('')
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid(sticky='new',pady=5,padx=5)
        # tk.Entry widget that displays the selected path and allows editing
        self.path_entry = ttk.Entry(self,textvariable=self.dir)
        self.path_entry.grid(column=0, row=0,sticky='we',padx=5,pady=5)
        self.path_entry.bind('<KeyRelease>', self.assert_dir) 
        # Browse directory button
        self.button = ttk.Button(self,text='Browse',command=self.select_dir)
        self.button.grid(column=1, row=0,sticky='we',padx=5,pady=5)
        # Error message only displayed  when validation fails
        self.error_label = ttk.Label(self,textvariable=self.error_msg,foreground='red')
        self.error_label.grid(column=0, row=1,sticky='we',padx=5)
        self.error_label.grid_remove()
        self.assert_dir()

    def select_dir(self):
        """ Allows the user to select a directory """
        path = Path(self.dir.get())
        if path.exists() and path.is_dir():
            filename=tk.filedialog.askdirectory(initialdir=path,title=f'Select a {self.title}')
        else:
            filename=tk.filedialog.askdirectory(initialdir='.',title=f'Select a {self.title}')
        if filename != path and filename != '':
            self.dir.set(filename)
            self.assert_dir()
    
    def assert_dir(self,event=None):
        """ Checks if the path entered is valid """
        path = Path(self.dir.get())
        if path.exists() and path.is_dir() and not self.dir.get() == '' and not self.dir.get() == '/':
            self.error_msg.set('')
            self.error_label.grid_remove()
            return True
        else:
            self.error_label.grid()
            self.error_msg.set('*Path does not exist or is not a directory.')
            return False