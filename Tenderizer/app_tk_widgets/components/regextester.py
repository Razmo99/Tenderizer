#!/usr/bin/env python3

"""Basic regular expression demonstration facility (Perl style syntax)."""

import tkinter as tk
import tkinter.ttk as ttk
import re
from typing import Text

class RegexTester:

    def __init__(self, master):
        self.master = master

        self.promptdisplay = ttk.Label(self.master, anchor=tk.W,
                text="Enter a Perl-style regular expression:")
        self.promptdisplay.pack(side=tk.TOP, fill=tk.X)

        self.regexdisplay = ttk.Entry(self.master)
        self.regexdisplay.pack(fill=tk.X)
        self.regexdisplay.focus_set()

        self.addoptions()

        self.statusdisplay = ttk.Label(self.master, text="", anchor=tk.W)
        self.statusdisplay.pack(side=tk.TOP, fill=tk.X)

        # Holds the Text display and its scroll bar
        self.textdisplay_frame=ttk.LabelFrame(self.master,text='Enter a string to search')
        self.textdisplay_frame.pack(fill=tk.BOTH,expand=1)

        self.showframe = ttk.Frame(self.textdisplay_frame)
        self.showframe.pack(fill=tk.X, anchor=tk.W)

        self.showvar = tk.StringVar(master)
        self.showvar.set("first")
        self.showfirstradio = ttk.Radiobutton(self.showframe,
                                         text="Highlight first match",
                                          variable=self.showvar,
                                          value="first",
                                          command=self.recompile)
        self.showfirstradio.pack(side=tk.LEFT)

        self.showallradio = ttk.Radiobutton(self.showframe,
                                        text="Highlight all matches",
                                        variable=self.showvar,
                                        value="all",
                                        command=self.recompile)
        self.showallradio.pack(side=tk.LEFT)
        # Text Display to enter in match data
        self.stringdisplay = tk.Text(self.textdisplay_frame, width=60, height=4)
        self.stringdisplay.pack(fill=tk.BOTH, expand=1,side=tk.LEFT)
        self.stringdisplay.tag_configure("hit", background="yellow")
        # Scroll bar for the text display
        self.text_scrollbar = ttk.Scrollbar(self.textdisplay_frame, orient=tk.VERTICAL, command=self.stringdisplay.yview)
        self.text_scrollbar.pack(fill=tk.BOTH, side=tk.LEFT)
        self.stringdisplay.configure(yscroll=self.text_scrollbar.set)
        # Holds the regex match groups and its scroll bar
        self.grouplist_frame=ttk.LabelFrame(self.master,text='Groups:')
        self.grouplist_frame.pack(fill=tk.BOTH,expand=1)
        # Holds all re match groups
        self.grouplist = tk.Listbox(self.grouplist_frame)
        self.grouplist.pack(expand=1, fill=tk.BOTH,side=tk.LEFT)
        
        self.grouplist_scrollbar = ttk.Scrollbar(self.grouplist_frame, orient=tk.VERTICAL, command=self.grouplist.yview)
        self.grouplist_scrollbar.pack(fill=tk.BOTH, side=tk.LEFT)
        self.grouplist.configure(yscroll=self.grouplist_scrollbar.set)        

        self.regexdisplay.bind('<Key>', self.recompile)
        self.stringdisplay.bind('<Key>', self.reevaluate)

        self.compiled = None
        self.recompile()

        btags = self.regexdisplay.bindtags()
        self.regexdisplay.bindtags(btags[1:] + btags[:1])

        btags = self.stringdisplay.bindtags()
        self.stringdisplay.bindtags(btags[1:] + btags[:1])
    
    def addoptions(self):
        self.frames = []
        self.boxes = []
        self.vars = []
        for name in ('IGNORECASE',
                     'MULTILINE',
                     'DOTALL',
                     'VERBOSE'):
            if len(self.boxes) % 3 == 0:
                frame = ttk.Frame(self.master)
                frame.pack(fill=tk.X)
                self.frames.append(frame)
            val = getattr(re, name).value
            var = tk.IntVar()
            box = ttk.Checkbutton(frame,
                    variable=var, text=name,
                    offvalue=0, onvalue=val,
                    command=self.recompile)
            box.pack(side=tk.LEFT)
            self.boxes.append(box)
            self.vars.append(var)

    def getflags(self):
        flags = 0
        for var in self.vars:
            flags = flags | var.get()
        return flags

    def recompile(self, event=None):
        try:
            self.compiled = re.compile(self.regexdisplay.get(),
                                       self.getflags())
            bg = self.promptdisplay['background']
            self.statusdisplay.config(text="", background=bg)
        except re.error as msg: 
            self.compiled = None
            self.statusdisplay.config(
                    text="re.error: %s" % str(msg),
                    background="red")
        self.reevaluate()

    def reevaluate(self, event=None):
        try:
            self.stringdisplay.tag_remove("hit", "1.0", tk.END)
        except tk.TclError:
            pass
        try:
            self.stringdisplay.tag_remove("hit0", "1.0", tk.END)
        except tk.TclError:
            pass
        self.grouplist.delete(0, tk.END)
        if not self.compiled:
            return
        self.stringdisplay.tag_configure("hit", background="yellow")
        self.stringdisplay.tag_configure("hit0", background="orange")
        text = self.stringdisplay.get("1.0", tk.END)
        last = 0
        nmatches = 0
        while last <= len(text):
            m = self.compiled.search(text, last)
            if m is None:
                break
            first, last = m.span()
            if last == first:
                last = first+1
                tag = "hit0"
            else:
                tag = "hit"
            pfirst = "1.0 + %d chars" % first
            plast = "1.0 + %d chars" % last
            self.stringdisplay.tag_add(tag, pfirst, plast)
            if nmatches == 0:
                self.stringdisplay.yview_pickplace(pfirst)
                groups = list(m.groups())
                groups.insert(0, m.group())
                for i in range(len(groups)):
                    g = "%2d: %r" % (i, groups[i])
                    self.grouplist.insert(tk.END, g)
            nmatches = nmatches + 1
            if self.showvar.get() == "first":
                break

        if nmatches == 0:
            self.statusdisplay.config(text="(no match)",
                                      background="yellow")
        else:
            self.statusdisplay.config(text="")


# Main function, run when invoked as a stand-alone Python program.

def main():
    root = tk.Tk()
    demo = RegexTester(root)
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.mainloop()

if __name__ == '__main__':
    main()