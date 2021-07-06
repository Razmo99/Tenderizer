from app_tk_widgets import BrowseDir
from tkintertestcase import TKinterTestCase

import tkinter as tk
import unittest

class TestBrowseDir(TKinterTestCase):
    
    """
    Goals of this class

    * Allow manual entry of a directory
    * Open a file dialog to select a directory
    * Check that the directory exists, display warning otherwise

    Produced information
    * Selected Directory
    * If the directory selected is valid

    Dependancies
    * None

    """

    def test_assert_dir(self):
        browse_dir = BrowseDir(self.root,'Input Directory')
        self.pump_events()
        browse_dir.entry.focus_set()
        browse_dir.entry.insert(tk.END,r'\\')
        browse_dir.assert_dir()
        self.pump_events()
        self.assertEqual(browse_dir.error_msg.get(),'')
        browse_dir.entry.insert(tk.END,r'/\\,><')
        browse_dir.assert_dir()
        self.pump_events()
        self.assertNotEqual(browse_dir.error_msg.get(),'')
        



