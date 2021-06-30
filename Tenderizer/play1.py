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
            self.string_arranger.get_duplicate_chars(self.string,self.dup_chars),
            self.expected_output)
    
    def test_get_dup_chars_end_only(self):
        self.string='test__'
        self.expected_output=[5]
        self.assertEqual(
            self.string_arranger.get_duplicate_chars(self.string,self.dup_chars),
            self.expected_output)

    def test_get_dup_chars_mid_only(self):
        self.string='te__st'
        self.expected_output=[3]
        self.assertEqual(
            self.string_arranger.get_duplicate_chars(self.string,self.dup_chars),
            self.expected_output)

    def test_get_dup_chars_start_and_end_only(self):
        self.string='__test__'
        self.expected_output=[1,7]
        self.assertEqual(
            self.string_arranger.get_duplicate_chars(self.string,self.dup_chars),
            self.expected_output)            

    def test_get_dup_chars_diff_chars(self):
        self.string='__test--test..'
        self.expected_output=[1,7,13]
        self.assertEqual(
            self.string_arranger.get_duplicate_chars(self.string,self.dup_chars),
            self.expected_output)     

    def test_get_dup_chars_multiple_chars(self):
        self.string='___test----test.....'
        self.expected_output=[1,2,8,9,10,16,17,18,19]
        self.assertEqual(
            self.string_arranger.get_duplicate_chars(self.string,self.dup_chars),
            self.expected_output)

    def test_get_non_dup_str_begin_only(self):
        self.string='__test'
        self.expected_output=['_','test']
        dup_chars_array=self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)
        self.assertEqual(
            self.string_arranger.get_non_dup_str(self.string,dup_chars_array),
            self.expected_output)
 
    def test_get_non_dup_str_end_only(self):
        self.string='test__'
        self.expected_output=['test_',]
        dup_chars_array=self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)
        self.assertEqual(
            self.string_arranger.get_non_dup_str(self.string,dup_chars_array),
            self.expected_output)
 
    def test_get_non_dup_str_end_only(self):
        self.string='te__st'
        self.expected_output=['te_','st']
        dup_chars_array=self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)
        self.assertEqual(
            self.string_arranger.get_non_dup_str(self.string,dup_chars_array),
            self.expected_output)
 
    def test_get_non_dup_str_start_and_end(self):
        self.string='__test__'
        self.expected_output=['_','test_']
        dup_chars_array=self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)
        self.assertEqual(
            self.string_arranger.get_non_dup_str(self.string,dup_chars_array),
            self.expected_output)

    def test_get_non_dup_str_multiple_chars(self):
        self.string='___test----test.....'
        self.expected_output=['_','test-','test.']
        dup_chars_array=self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)
        self.assertEqual(
            self.string_arranger.get_non_dup_str(self.string,dup_chars_array),
            self.expected_output)

    def test_get_non_dup_str_multiple_chars(self):
        self.string='   Electrical Services   Lighting and Controls Refle/cted Ceiling Plan Level 5'
        self.expected_output=[' ','Electrical Services ','Lighting and Controls Refle/cted Ceiling Plan Level 5']
        dup_chars_array=self.string_arranger.get_duplicate_chars(self.string,self.dup_chars)
        self.assertEqual(
            self.string_arranger.get_non_dup_str(self.string,dup_chars_array),
            self.expected_output)

if __name__ == '__main__':
    from timeit import timeit
    def job():
        sa=StringArranger()
        sa.get_duplicate_chars('  Elect  rical Services  Ligh  ting and Co  ntrols Refle/cted Ceiling Plan Level 5',['-','_',' ','.'])
    print(timeit(lambda: job(),number=1_000_000))
    #unittest.main()