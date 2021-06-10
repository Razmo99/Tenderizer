import logging
import logging.handlers
import tkinter.filedialog
import tkinter as tk
from tkinter.constants import CENTER
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)

class TreeView(ttk.LabelFrame):

    def __init__(self, master,lf_title,column):
        ttk.LabelFrame.__init__(self,master,text=lf_title)

        self.grid(sticky='nsew',pady=5,padx=5)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        # Hold the Treeview and scroll bar. Keeps them together
        self.container=ttk.Frame(self)
        self.container.grid(sticky='nsew',pady=5,padx=5,row=1,column=0,ipady=5,ipadx=5)
        # Make the tree ciew have priority for screen resizing
        self.container.grid_rowconfigure(0,weight=0)
        self.container.grid_rowconfigure(1,weight=1)
        self.container.grid_rowconfigure(2,weight=0)
        self.container.grid_columnconfigure(0,weight=1)

        self.tree = ttk.Treeview(self.container,columns=column,show='headings')
        # Scroll bar for tree view
        self.scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1,sticky='nsew')

        # create columns and headers based on input
        [self.tree.column(col,stretch=tk.YES) for col in column]
        [self.tree.heading(col,text=col,anchor=CENTER,command=lambda _col=col:self.sort_column(self.tree,_col,False)) for col in column]
        self.tree.grid(row=1,column=0,sticky='nsew')

        # Button to load Directory
        self.load_button= ttk.Button(self,text='Load',command=self.master.load_pdfs,state='disabled')
        self.load_button.grid(row=0,column=0,sticky='nw',padx=5,pady=5)
        # Button to Convert Directory
        self.convert_button=ttk.Button(self,text='Convert',command=self.master.convert_paths,state='disabled')
        self.convert_button.grid(row=2,column=0,padx=5,pady=5,sticky='nw')        

    def sort_column(self,tv, col, reverse):
        """ Sorts Columns in a tree view"""
        # Source https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, text=col, command=lambda _col=col: \
                    self.sort_column(tv, _col, not reverse))