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
        
        self.match_order=[]
        self.selection_preview=[]
        self.deliminator_options={
            'Hyphen':'-',
            'Space':' ',
            'Underscore':'_'
        }

        self.new_tree_view_frame()
        self.new_tree_view()
        self.new_tree_view_scrollbar()

        self.new_details_frame()
        self.new_selection_entry()

        self.new_deliminator_frame()
        self.new_deliminator_option_menu()

        # Displays an example of what the selection will look like
        self.selection_preview_label = ttk.Label(self.details_frame, text='Nothing to display yet.',wraplength=300,justify=tk.LEFT)
        self.selection_preview_label.grid(sticky='nwe',pady=5,padx=5,row=3,column=0)

    def new_tree_view(self):
        """ Create treeview with columns and headers"""
        self.tree = ttk.Treeview(self.tv_frame,columns=['ID','Example Value'],show='headings')
        
        self.tree.column('ID',stretch=tk.YES,width=10)
        self.tree.heading('ID',text='ID',anchor=tk.CENTER)
        self.tree.column('Example Value',stretch=tk.YES)
        self.tree.heading('Example Value',text='Example Value',anchor=tk.CENTER)
        self.tree.grid(row=0,column=0,sticky='nsew')

    def new_tree_view_scrollbar(self):
        """Scroll bar for tree view"""
        self.scrollbar = ttk.Scrollbar(self.tv_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1,sticky='nsew')        

    def new_selection_entry(self):
        """ Entry for the user to select re match groups"""
        # Descriptions for the match order selection entry
        self.entry_label = ttk.Label(self.details_frame, text='Enter in any combination of ID(s)\n seperated by a comma, from the View to the left.',wraplength=300,justify=tk.LEFT)
        self.entry_label.grid(sticky='nwe',pady=5,padx=5,row=0,column=0)
        # Hold the re match selection string
        self.var=tk.StringVar(self)
        # Entry widget to type the re match selection into
        self.entry=ttk.Entry(self.details_frame,textvariable=self.var,width=25,foreground='grey')
        self.entry.grid(sticky='nw',pady=5,padx=5,row=1,column=0)
        self.entry.insert(0,'1,2')
        self.entry.bind('<FocusIn>',self.remove_entry_tip)
        self.entry.bind('<KeyRelease>', self.compare_user_input)

    def new_deliminator_option_menu(self):
        """Spinbox that lets the user select the regex match deliminator"""
        self.deliminator_label = ttk.Label(self.deliminator_frame,text='Deliminator:')
        self.deliminator_label.grid(row=0,column=0,sticky="nw",padx=5,pady=5)

        self.deliminator_var=tk.StringVar()
        self.deliminator=ttk.OptionMenu(self.deliminator_frame,
            self.deliminator_var,
            'Choose',
            *self.deliminator_options.keys(),
            direction='below',
            command=self.on_deliminator_selection)
        self.deliminator.grid(row=0,column=1,sticky="nw",padx=5,pady=5)

    def new_deliminator_frame(self):
        """Hold re deliminator spinbox"""
        self.deliminator_frame = ttk.Frame(self.details_frame)
        self.deliminator_frame.grid(sticky='nw',row=2,column=0)
        self.deliminator_frame.grid_rowconfigure(0,weight=1)
        self.deliminator_frame.grid_columnconfigure(0,weight=1)

    def new_details_frame(self):
        """Contains the user entry and results display"""
        self.details_frame=ttk.LabelFrame(self,text='RE Match Order')
        self.details_frame.grid(sticky='nsew',pady=5,padx=5,row=0,column=1)

    def new_tree_view_frame(self):
        """" Holds the Treeview and scroll bar"""
        self.tv_frame=ttk.LabelFrame(self,text='Available RE Match Groups')
        self.tv_frame.grid(sticky='nsew',pady=5,padx=5,row=0,column=0,ipadx=5,ipady=5)
        # Make the tree view have priority for screen resizing
        self.tv_frame.grid_rowconfigure(0,weight=1)
        self.tv_frame.grid_columnconfigure(0,weight=1)
    
    def add_tree_view_items(self,groups):
        """ Adds items to the tree view  """
        for key,value in groups.items():
            tv_values=[key,value[:25]]
            self.tree.insert('','end',iid=key,values=tv_values)

    def compare_user_input(self,event=None):
        # Clear the existing match_order and selection_preview
        del self.match_order[:]
        del self.selection_preview[:]

        self.update_selections()
        self.update_selection_preview()

    def update_selection_preview(self):
        """ Update the selection preview """
        # make sure we got something
        if self.selection_preview:
            # remove tail deliminator
            del self.selection_preview[-1]
            # Set the preview label to display the results
            self.selection_preview_label.configure(text=''.join(self.selection_preview))
        else:
            # No matches found let display on the gui
            self.selection_preview_label.configure(text='No Matches')

    def update_selections(self):
        """ Makes sure that the selections entered are valid re Match Groups"""
        # Get the current selections
        selections=self.entry.get().split(',')
        # Get the treeview's ID's
        tv_ids=self.tree.get_children()
        # Set the deliminator
        selection_deliminator=self.deliminator_options.get(self.deliminator_var.get())
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
                if selection_deliminator:
                    self.selection_preview.append(selection_deliminator)
                else:
                    # Get the first deliminator in the available options
                    first_key=next(iter(self.deliminator_options))
                    self.selection_preview.append(self.deliminator_options.get(first_key))

    def remove_entry_tip(self,event=None):
        """Gets called once the entry field is clicked then unbinds itself"""
        if self.entry.get() == '1,2':
            self.entry.delete(0,'end')
            self.entry.insert(0,'')
            self.entry.configure(foreground='black')
            self.entry.unbind(self.remove_entry_tip)

    def on_deliminator_selection(self,val):
        self.compare_user_input()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegexMatchOrder(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.option_add('*tearOff', tk.FALSE)
    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)

    groups = {1:'Cheese',2:'Baked',3:'Cake'}
    app.add_tree_view_items(groups)

    root.mainloop()    