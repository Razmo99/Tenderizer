import tkinter as tk
import tkinter.ttk as ttk
import logging
import json
from pathlib import Path, PurePath
from ..components import RegexEntry, TreeView, RegexMatchOrder,RegexTester
from ..utilities import FileNamer
import re
class RegexMatcher(ttk.Frame):

    def __init__(self,master):

        ttk.Frame.__init__(self,master)
        self.dataset=self.master.dataset

        self.grid(row=0,column=0,sticky='nsew')
        self.grid_rowconfigure(0,weight=5)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        
        self.regex_entry = RegexEntry(self)
        self.regex_entry.grid(row=0,column=0)

        self.file_namer = FileNamer(
            re.compile(r'(\-|\_|\ |\.)+',flags=re.S|re.M),
            re.compile(r'[\/\\\|\<\>\?\"\*\:\,]+',flags=re.S|re.M))

        self.match_group_selector=RegexMatchOrder(self.regex_entry,self.file_namer)
        self.match_group_selector.grid(sticky='nsew',row=6,column=0)
        self.new_match_ordered_name=self.file_namer.new_file_name
        self.new_match_order_examples=self.match_group_selector.add_tree_view_items

        self.treeview = TreeView(self,'Match View',('Name','New Name'))
        self.treeview.grid(row=1,column=0)
        
        self.treeview.load_button.configure(command=self.set_files_new_name,state='normal')
        self.treeview.convert_button.configure(command=self.rename_files,state='normal',text='Rename')

        self.treeview.right_click_selection_menu.add_command(label='Regex Utility',command=lambda :self.open_regex_util())

    def set_files_new_name(self):
        """ Evaluates the dataset against the input re expression """
        dataset=self.dataset
        if dataset:
            self.treeview.tree.delete(*self.treeview.tree.get_children())
            for pdf in dataset:
                tv_new_name=self.search_re_expression(pdf)
                if isinstance(tv_new_name,str):
                    tv_new_name = tv_new_name[:512]
                self.treeview.tree.insert('','end',iid=pdf.id,values=[pdf.name,tv_new_name])
            if dataset[1].converted and dataset[1].regex_matches:
                self.new_match_order_examples(dataset[1].regex_matches)
    
    def get_compiled_re(self):
        """ Checks that the re is compiled and no syntax warnings are present"""
        re_compiled = self.regex_entry.compiled
        re_compiled_status = self.regex_entry.statusdisplay.cget('text')
        if  re_compiled_status == "" and re_compiled:
            return re_compiled
    
    def search_re_expression(self, pdf):
        if pdf.converted:
            # Check if the regex entry is valid and compiled
            compiled_regex=self.get_compiled_re()
            if compiled_regex:
                re_match=compiled_regex.search(pdf.text_data)
                if not re_match is None:
                    pdf.regex_matches=re_match
                    suffix=pdf.input_path.suffix
                    prefix=pdf.name.replace(suffix,'')
                    new_file_name = self.new_match_ordered_name(prefix,suffix,re_match)
                    if new_file_name:
                        pdf.new_name=new_file_name
                        return new_file_name

    def rename_files(self):
        if self.dataset:
            for pdf in self.dataset:
                input_path=Path(pdf.input_path)
                rename_path=input_path.parent / pdf.new_name
                output={
                    'operation': 'rename',
                    'input_path': f'{input_path.resolve()}',
                    'rename_path': f'{rename_path.resolve()}',
                    'completed': True
                }
                try:
                    pdf.rename_op=(input_path,rename_path)
                    input_path.rename(rename_path)
                except:
                    output['completed']=False
                    logging.exception(json.dumps(output))
                    raise
                else:
                    logging.info(json.dumps(output))
    
    def open_regex_util(self):
        x=tk.Toplevel(self.master)
        x.title('Regex Tester')
        selection = self.treeview.tree.selection()
        text_data=''
        for pdf in self.dataset:
            if pdf.id == selection[0]:
                text_data=pdf.text_data

        self.regex_tester = RegexTester(x)
        self.regex_tester.regexdisplay.delete(0,tk.END)
        self.regex_tester.regexdisplay.insert(0,self.regex_entry.var.get())
        self.regex_tester.stringdisplay.delete(1.0,tk.END)
        self.regex_tester.stringdisplay.insert(1.0,text_data)
        for i,val in enumerate(self.regex_tester.vars):
            val.set(self.regex_entry.vars[i].get())
        self.regex_tester.recompile()