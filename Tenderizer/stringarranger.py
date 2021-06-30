import unittest

class StringArranger():
    
    def get_duplicate_chars(self,string,dup_chars):
        str_len=len(string) - 1
        results=[]
        for index,char in enumerate(string):
            if char in dup_chars:
                if index < str_len:
                    ahead=index+1
                else:
                    ahead=index
                #ahead=index+1 if index < str_len else index
                if index < str_len and string[ahead] == char:
                    results.append(ahead)
        return results

    def get_non_dup_str(self,string,dup_chars_array):
        str_len=len(string) - 1
        array_len=len(dup_chars_array)
        results=[]
        prev_dup_char=None
        for dup_index,dup_char in enumerate(dup_chars_array):
            if dup_index > 0 and dup_index < array_len:
                prev_dup_char=dup_chars_array[dup_index-1]+1
            behind = dup_char
            if string[prev_dup_char:behind]:
                results.append(string[prev_dup_char:behind])
        if dup_chars_array[-1] < str_len:
            results.append(string[dup_chars_array[-1]+1:])
        return results


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
    unittest.main()        