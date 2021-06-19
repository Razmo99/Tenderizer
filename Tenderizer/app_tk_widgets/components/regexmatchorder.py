from os import stat
import tkinter as tk
import tkinter.ttk as ttk

class RegexMatchOrder(ttk.Labelframe):
    """Class that facilitates the ordering or regex matches"""

    def __init__(self ,master):
        # Init the parent frame and grid it.
        ttk.Frame.__init__(self,master)
        self.grid(sticky='nsew',padx=5,pady=5)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        # Holds the Treeview and scroll bar.
        self.tv_frame=ttk.LabelFrame(self,text='Available RE Match Groups')
        self.tv_frame.grid(sticky='nsew',pady=5,padx=5,row=0,column=0,ipadx=5,ipady=5)
        # Make the tree view have priority for screen resizing
        self.tv_frame.grid_rowconfigure(0,weight=1)
        self.tv_frame.grid_columnconfigure(0,weight=1)
        self.tree = ttk.Treeview(self.tv_frame,columns=['ID','Example Value'],show='headings')
        # Scroll bar for tree view
        self.scrollbar = ttk.Scrollbar(self.tv_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1,sticky='nsew')

        # Create columns and headers based on input
        self.tree.column('ID',stretch=tk.YES,width=10)
        self.tree.heading('ID',text='ID',anchor=tk.CENTER)
        self.tree.column('Example Value',stretch=tk.YES)
        self.tree.heading('Example Value',text='Example Value',anchor=tk.CENTER)
        self.tree.grid(row=0,column=0,sticky='nsew')

        # Contains the user entry and results display
        self.details_frame=ttk.LabelFrame(self,text='RE Match Order')
        self.details_frame.grid(sticky='nsew',pady=5,padx=5,row=0,column=1)
        # Descriptions for the match order selection entry
        self.entry_label = ttk.Label(self.details_frame, text='Enter in any combination of ID(s)\n seperated by a comma, from the View to the left.',wraplength=300,justify=tk.LEFT)
        self.entry_label.grid(sticky='nwe',pady=5,padx=5,row=0,column=1)
        self.bg=self.entry_label['background']

        # Hold the re match selection string
        self.var=tk.StringVar(self)
        # Entry widget to type the re match selection into
        self.entry=ttk.Entry(self.details_frame,textvariable=self.var,width=25,foreground='grey')
        self.entry.grid(sticky='nw',pady=5,padx=5,row=1,column=1)

        self.entry.insert(0,'1,2')
        self.entry.bind('<FocusIn>',self.on_entry_click)

        # Displays an example of what the selection will look like
        self.statusdisplay = ttk.Label(self.details_frame, text='Nothing to display yet.',wraplength=300,justify=tk.LEFT)
        self.statusdisplay.grid(sticky='nwe',pady=5,padx=5,row=2,column=1)
        
        self.entry.bind('<KeyRelease>', self.evauluate)
        self.match_order=[]
        self.selection_preview=[]
    
    def populate_tv(self,groups):
        for key,value in groups.items():
            tv_values=[key,value[:25]]
            self.tree.insert('','end',iid=key,values=tv_values)

    def evauluate(self,event=None):
        # Clear the existing match_order and selection_preview
        del self.match_order[:]
        del self.selection_preview[:]
        # Get the current selections
        selections=self.entry.get().split(',')
        # Get the treeview's ID's
        tv_ids=self.tree.get_children()
        # Set the deliminator
        selection_deliminator='-'
        # Iterate over the split selections
        for selection in selections:
            # Check the selection exists in the tree view ids
            if selection in tv_ids:
                #Add the selection to the match order which is used by a parent class
                self.match_order.append(selection)
                # Grab row values from the tree view
                tv_values=self.tree.set(selection)
                # append the tree view value above to the selection preview
                self.selection_preview.append(tv_values['Example Value'])
                # append the deliminator
                self.selection_preview.append(selection_deliminator)
        # make sure we got something
        if self.selection_preview:
            # remove tail deliminator
            del self.selection_preview[-1]
            # Set the preview label to display the results
            self.statusdisplay.configure(text=''.join(self.selection_preview))
        else:
            # No matches found let display on the gui
            self.statusdisplay.configure(text='No Matches')

    def on_entry_click(self,event=None):
        """Gets called whenever the entry field is clicked"""
        if self.entry.get() == '1,2':
            self.entry.delete(0,'end')
            self.entry.insert(0,'')
            self.entry.configure(foreground='black')
            self.entry.unbind(self.on_entry_click)






if __name__ == "__main__":
    root = tk.Tk()
    app = RegexMatchOrder(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.option_add('*tearOff', tk.FALSE)
    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)

    groups = {1:'Cheese',2:'Baked',3:'Cake'}
    app.populate_tv(groups)

    root.mainloop()    