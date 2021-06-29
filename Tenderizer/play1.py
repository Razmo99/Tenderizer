import re

import unittest
from unittest.case import expectedFailure

from stringarranger import StringArranger

    
class TestStringArranger(unittest.TestCase):

    def setUp(self):
        self.string_arranger=StringArranger()
        self.dup_chars=['-','_',' ','.']

    def test_get_dup_chars_begin_only(self):
        self.string='__test'
        self.expected_output=[1]
        self.assertEqual(
            list(self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)),
            self.expected_output)
    
    def test_get_dup_chars_end_only(self):
        self.string='test__'
        self.expected_output=[5]
        self.assertEqual(
            list(self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)),
            self.expected_output)

    def test_get_dup_chars_mid_only(self):
        self.string='te__st'
        self.expected_output=[3]
        self.assertEqual(
            list(self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)),
            self.expected_output)

    def test_get_dup_chars_start_and_end_only(self):
        self.string='__test__'
        self.expected_output=[1,7]
        self.assertEqual(
            list(self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)),
            self.expected_output)            

    def test_get_dup_chars_diff_chars(self):
        self.string='__test--test..'
        self.expected_output=[1,7,13]
        self.assertEqual(
            list(self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)),
            self.expected_output)     

    def test_get_dup_chars_multiple_chars(self):
        self.string='___test----test.....'
        self.expected_output=[1,2,8,9,10,16,17,18,19]
        self.assertEqual(
            list(self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)),
            self.expected_output)
if __name__ == '__main__':
    unittest.main()