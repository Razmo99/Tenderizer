from unittest.case import expectedFailure
from app_tk_widgets import RegexMatchOrder
from tkintertestcase import TKinterTestCase
import re
import tkinter as tk
import unittest

class TestRegexEntry(TKinterTestCase):
    """
    Goals of this class

    * Input of RE Match Group ID's to assemble a string
    * Display a preview of the assembled string
    * Selection of the Deliminator

    Produced information
    * Match Order
     * array of ints

    Dependancies
    * None

    """

    def test_add_tree_view_items(self):
        re_match_order = RegexMatchOrder(self.root)
        self.str_multiple_match_groups='Drawing Title\nServices - \n\nLighting and\n\n Controls Level 6\n\nScale at A1\n\nRev\n\n05'
        expected_result=[
            ('Services - Lighting and Controls Level 6', '1'),
            ('Rev','2'),
            ('05','3')
        ]
        self.pump_events()
        self.match=re.search(
            r'Drawing Title(.*)Scale at A1.*?(Rev).*?(\d+)',
            self.str_multiple_match_groups,
            flags=re.M|re.S)
        re_match_order.add_tree_view_items(self.match)
        self.pump_events()
        tv=re_match_order.tree
        l = [(tv.set(k, 'Example Value'), k) for k in tv.get_children('')]
        self.pump_events()
        self.assertEquals(expected_result,l)

    def test_match_order_preview(self):
        re_match_order = RegexMatchOrder(self.root)
        re_match_order = RegexMatchOrder(self.root)
        entry=re_match_order.entry
        self.str_multiple_match_groups='Drawing Title\nServices - \n\nLighting and\n\n Controls Level 6\n\nScale at A1\n\nRev\n\n05'
        expected_result='Services Lighting and Controls Level 6 Rev 05'
        self.match=re.search(
            r'Drawing Title(.*)Scale at A1.*?(Rev).*?(\d+)',
            self.str_multiple_match_groups,
            flags=re.M|re.S)
        re_match_order.add_tree_view_items(self.match)
        entry.event_generate('<FocusIn>')
        self.pump_events()
        self.assertEquals('',entry.get())
        entry.insert(tk.END,'1,2,3')
        entry.event_generate('<KeyRelease>')
        re_match_order.option_menu_var.set('Space')
        re_match_order.compare_user_input()
        self.pump_events()
        self.assertEquals(
            re_match_order.preview_label_var.get(),
            expected_result)
        self.assertEquals([1,2,3],re_match_order.match_order)



