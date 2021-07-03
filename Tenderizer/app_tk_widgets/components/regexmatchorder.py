import logging
import tkinter as tk
import tkinter.ttk as ttk
import re
import logging
from ..utilities import FileNamer
logger = logging.getLogger(__name__)

class RegexMatchOrder(ttk.Labelframe):
    """Class that facilitates the ordering or regex matches"""

    def __init__(self ,master,filenamer=None) -> None:
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
            'Underscore':'_',
            'Period':'.'
        }
        if filenamer:
            self.filenamer=filenamer
        else:
            self.filenamer=FileNamer(
                re.compile(r"(\-|\_|\ |\.)+",flags=re.M|re.S),
                re.compile(r"(\n|\r|\r\n)+",flags=re.M|re.S),
            )

        self.new_tree_view_frame()
        self.new_tree_view()
        self.new_tree_view_scrollbar()

        self.new_details_frame()
        self.new_selection_entry()

        self.new_deliminator_frame()
        self.new_deliminator_option_menu()

        # Displays an example of what the selection will look like
        self.preview_label_var = tk.StringVar(self)
        self.preview_label = ttk.Label(self.details_frame, textvariable=self.preview_label_var,wraplength=300,justify=tk.LEFT)
        self.preview_label.grid(sticky='nwe',pady=5,padx=5,row=3,column=0)
        self.preview_label_var.set('Nothing to display yet.')

    def new_tree_view(self):
        """ Create treeview with columns and headers"""
        self.tree = ttk.Treeview(self.tv_frame,columns=['ID','Example Value'],show='headings')
        
        self.tree.column('ID',stretch=tk.NO,width=50)
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
        self.entry_label = ttk.Label(self.details_frame, text='From the View to the left, enter in any combination of ID(s)\n seperated by a comma.',wraplength=300,justify=tk.LEFT)
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
        self.option_menu_label = ttk.Label(self.deliminator_frame,text='Deliminator:')
        self.option_menu_label.grid(row=0,column=0,sticky="nw",padx=5,pady=5)

        self.option_menu_var=tk.StringVar()
        self.option_menu=ttk.OptionMenu(self.deliminator_frame,
            self.option_menu_var,
            'Choose',
            *self.deliminator_options.keys(),
            direction='below',
            command=self.on_deliminator_selection)
        self.option_menu.grid(row=0,column=1,sticky="nw",padx=5,pady=5)

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
    
    def add_tree_view_items(self,match):
        """ Adds items to the tree view  """
        self.tree.delete(*self.tree.get_children())
        for index,group in enumerate(match.groups(),start=1):
            example_value=self.filenamer.remove_newline(group)
            tv_values=[index,example_value.strip()]
            self.tree.insert('','end',iid=index,values=tv_values)
        self.compare_user_input

    def compare_user_input(self,event=None):
        """ Compare user input against the tree view
            Refeshes the selection preview
         """
        # Clear the existing match_order and selection_preview
        del self.match_order[:]
        del self.selection_preview[:]

        self.update_selections()
        self.update_selection_preview()

    def update_selection_preview(self):
        """ Update the selection preview """
        if self.selection_preview:
            # remove tail deliminator
            del self.selection_preview[-1]
            self.filenamer.deliminator=self.get_deliminator()
            self.filenamer.match_order=self.match_order
            preview_text=''.join(self.filenamer.set_match_deliminator(self.selection_preview))

            if len(preview_text) > 1024:
                self.preview_label.configure(foreground='red')
            else:
                self.preview_label.configure(foreground='')
            self.preview_label_var.set(preview_text[:1024])
        else:
            self.preview_label_var.set('No Matches')

    def update_selections(self):
        """ Makes sure that the selections entered are valid re Match Groups"""
        selections=self.entry.get().split(',')
        tv_ids=self.tree.get_children()
        for selection in selections:
            if selection in tv_ids:
                self.match_order.append(int(selection))
                tv_values=self.tree.set(selection)
                self.selection_preview.append(tv_values['Example Value'][:512])
                self.selection_preview.append(self.get_deliminator())

    def get_deliminator(self):
        """ return the selected deliminator or 
        returns the first deliminator in the available options if no option is choosen yet """
        current_selection=self.deliminator_options.get(self.option_menu_var.get())
        if current_selection:
            return current_selection
        else:
            first_key=next(iter(self.deliminator_options))
            return self.deliminator_options.get(first_key)

    def remove_entry_tip(self,event=None):
        """Gets called once the entry field is clicked then unbinds itself"""
        if self.entry.get() == '1,2':
            self.entry.delete(0,'end')
            self.entry.insert(0,'')
            self.entry.configure(foreground='black')
            self.entry.unbind('<FocusIn>')

    def on_deliminator_selection(self,val):
        self.compare_user_input()        