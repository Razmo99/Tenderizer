import tkinter as tk
import _tkinter as _tk
import tkinter.ttk as ttk
import unittest

class TKinterTestCase(unittest.TestCase):
    #Source https://stackoverflow.com/questions/4083796/how-do-i-run-unittest-on-a-tkinter-app
    """These methods are going to be the same for every GUI test,
    so refactored them into a separate class
    """
    def setUp(self):
        self.root=tk.Tk()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.dooneevent(_tk.ALL_EVENTS | _tk.DONT_WAIT):
            pass