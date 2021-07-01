import tkinter as tk
import tkinter.ttk as ttk
import re

"""
Goals of this class

* Manual input and calidation of regex
* Selection of regex Flags

Produced information
* Compiled regex object

Dependancies
* None

"""

class RegexEntry(ttk.Labelframe):
    """Class that holds a entry box for regular expression with flags"""
    # This is a chopped up copy of regex tester demo on python.org
    def __init__(self,master):
        # Init the parent frame for this call that all widgets will sit in
        ttk.LabelFrame.__init__(self,master,text='Regular Expression')
        self.grid(sticky='nsew',padx=5,pady=5)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(6,weight=1)

        self.compiled=None
        self.new_status_display_label()
        self.new_re_entry()

        # This adds all the check boxes for re flags
        self.addoptions()
        self.recompile()

    def new_status_display_label(self):
        """ Displays any re compile errors """
        self.statusdisplay = ttk.Label(self, text='')
        self.statusdisplay.grid(sticky='nwe',pady=5,padx=5,row=0,column=0,ipadx=5,ipady=5)
        self.bg=self.statusdisplay['background']

    def new_re_entry(self):
        """ Entry the re string """
        self.var=tk.StringVar(self)
        # Entry widget to type the re into
        self.entry=ttk.Entry(self,textvariable=self.var)
        self.entry.grid(sticky='nwe',pady=5,padx=5,row=1,column=0)
        # Recomplile the regular expression every time a key is pressed in the entry widget
        self.entry.bind('<KeyRelease>', self.recompile)        
    
    def addoptions(self):
        """Adds re Flags under regex entry"""
        self.frames = []
        self.boxes = []
        self.vars = []
        for index,name in enumerate(('IGNORECASE',
                     'MULTILINE',
                     'DOTALL',
                     'VERBOSE'),start=1):
            if len(self.boxes) % 3 == 0:
                frame = ttk.Frame(self)
                frame.grid(sticky='nw')
                self.frames.append(frame)
            val = getattr(tk.re, name).value
            var = tk.IntVar()
            box = ttk.Checkbutton(frame,
                    variable=var, text=name,
                    offvalue=0, onvalue=val,
                    command=self.recompile)

            box.grid(sticky='nw',row=2,column=index)
            self.boxes.append(box)
            self.vars.append(var)

    def getflags(self):
        """Retreives re flags from checkboxes under regex entry"""
        flags = 0
        for var in self.vars:
            flags = flags | var.get()
        return flags        

    def recompile(self, event=None):
        """Recompliles the Regular Expression and updates the statusdisplay"""
        try:
            self.compiled = re.compile(self.entry.get(),
                                       self.getflags())
            self.statusdisplay.config(text="", background=self.bg)
        except tk.re.error as msg:
            self.compiled = None
            self.statusdisplay.config(
                    text=f"re.error: {str(msg)}",
                    background="red")
