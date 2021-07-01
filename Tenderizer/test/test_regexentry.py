from app_tk_widgets import RegexEntry
from tkintertestcase import TKinterTestCase

import tkinter as tk
import unittest

class TestRegexEntry(TKinterTestCase):
    """
    Goals of this class

    * Manual input and validation of regex
    * Selection of regex Flags

    Produced information
    * Compiled regex object

    Dependancies
    * None

    """

    def test_invalid_re_warning(self):
        regex = RegexEntry(self.root)
        self.pump_events()
        regex.entry.focus_set()
        regex.entry.insert(tk.END,'(')
        regex.recompile()
        self.pump_events()
        self.assertNotEqual(regex.statusdisplay.cget('text'),'')
        regex.entry.insert(tk.END,')')
        regex.recompile()
        self.pump_events()
        self.assertEqual(regex.statusdisplay.cget('text'),'')
        self.assertNotEqual(regex.compiled,None)

    def test_flag_selection(self):
        pass



