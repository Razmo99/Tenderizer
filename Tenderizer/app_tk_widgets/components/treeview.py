import logging
import logging.handlers
import tkinter.filedialog
import tkinter as tk
from tkinter.constants import CENTER
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)

class RightClickSelection(tk.Menu):
    """" Displays a menu with options for when multiple items are selected """
    def __init__(self, master):
        tk.Menu.__init__(self,master,tearoff=False)
        self.add_command(label='Delete Selection',command=lambda :self.master.delete_selection())

class TreeView(ttk.LabelFrame):

    def __init__(self, master,lf_title,column):
        ttk.LabelFrame.__init__(self,master,text=lf_title)

        self.grid(sticky='nsew',pady=5,padx=5)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        # Hold the Treeview and scroll bar. Keeps them together
        self.tv_frame=ttk.Frame(self)
        self.tv_frame.grid(sticky='nsew',pady=5,padx=5,row=1,column=0,ipady=5,ipadx=5)
        # Make the tree ciew have priority for screen resizing
        self.tv_frame.grid_rowconfigure(0,weight=0)
        self.tv_frame.grid_rowconfigure(1,weight=1)
        self.tv_frame.grid_rowconfigure(2,weight=0)
        self.tv_frame.grid_columnconfigure(0,weight=1)

        self.tree = ttk.Treeview(self.tv_frame,columns=column,show='headings')
        # Scroll bar for tree view
        self.scrollbar = ttk.Scrollbar(self.tv_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1,sticky='nsew')

        # create columns and headers based on input
        [self.tree.column(col,stretch=tk.YES) for col in column]
        [self.tree.heading(col,text=col,anchor=CENTER,command=lambda _col=col:self.sort_column(self.tree,_col,False)) for col in column]
        self.tree.grid(row=1,column=0,sticky='nsew')

        # Button to load Directory
        self.load_frame = ttk.Frame(self)
        self.load_frame.grid(sticky='nw',row=0,column=0)
        self.load_frame.grid_rowconfigure(1,weight=1)
        self.load_frame.grid_columnconfigure(0,weight=1)

        self.load_button = ttk.Button(self.load_frame,text='Load',state=tk.DISABLED)
        self.load_button.grid(row=0,column=0,sticky='nw',padx=5,pady=5)
        # Button to Convert Directory
        self.converted_frame = ttk.Frame(self)
        self.converted_frame.grid(sticky='nw',row=2,column=0)
        self.converted_frame.grid_rowconfigure(1,weight=1)
        self.converted_frame.grid_columnconfigure(0,weight=1)

        self.convert_button=ttk.Button(self.converted_frame,text='Convert',state=tk.DISABLED)
        self.convert_button.grid(row=2,column=0,padx=5,pady=5,sticky='nw')
        
        self.right_click_selection_menu = RightClickSelection(self)
        # When an item is right clicked bring up a menu
        self.tree.bind('<Button-3>', self.right_click)     

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
    
    def right_click(self, event):
        selection = self.tree.selection()
        if selection:
            self.right_click_selection_menu.post(event.x_root,event.y_root)         
        else:
            pass

    def delete_selection(self):
        # list of pdf data classes
        dataset = self.master.dataset
        # current selection in the tree view
        selection = self.tree.selection()
        # Check the tree view has a data set
        if dataset:
            # iterate over the current selection
            for iid in selection:
                # iterate over the data set
                for index,pdf in enumerate(dataset):
                    # look for an ID match
                    if iid == pdf.id:
                        # remove the item from the dataset
                        del dataset[index]
        # Remove the selection from the tree view
        self.tree.delete(*self.tree.selection())
