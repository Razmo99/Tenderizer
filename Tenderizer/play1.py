import re
import unittest


class RegexStringArranger():

    def __init__(self,regular_expression) -> None:
        self.regular_expression=regular_expression
    
    def get_dup_str(self,string):
        return re.finditer(
            self.regular_expression,
            string)

    def remove_dup_chars(self,string,dup_chars):
        str_len=len(string)
        results=['_test']
        re_matches=list(dup_chars)
        re_matches_len=len(re_matches)
        prev_span_end=None
        for index_,re_match in enumerate(re_matches):

            s_begin,s_end=re_match.span()
            results.append(prev_span_end:behind)
        return results

class TestRegexStringArranger(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_get_dup_chars_begin(self):
        expression = re.compile(r"(\-|\_|\ |\.)\1+",flags=re.M|re.S)
        re_arranger = RegexStringArranger(expression)
        string='__test'
        dup_str=list(re_arranger.get_dup_str(string))
        self.assertEqual((0,2),dup_str[0].span())

    def test_get_dup_chars_begin_end(self):
        expression = re.compile(r"(\-|\_|\ |\.)\1+",flags=re.M|re.S)
        re_arranger = RegexStringArranger(expression)
        string='__test--'
        dup_str=list(re_arranger.get_dup_str(string))
        self.assertEqual((0,2),dup_str[0].span())        
        self.assertEqual((6,8),dup_str[1].span())

    def test_get_dup_chars_begin_mid_end(self):
        expression = re.compile(r"(\-|\_|\ |\.)\1+",flags=re.M|re.S)
        re_arranger = RegexStringArranger(expression)
        string='__te---st--'
        dup_str=list(re_arranger.get_dup_str(string))
        self.assertEqual((0,2),dup_str[0].span())
        self.assertEqual((4,7),dup_str[1].span())           
        self.assertEqual((9,11),dup_str[2].span())

    def test_remove_dup_chars_begin(self):
        expression = re.compile(r"(\-|\_|\ |\.)\1+",flags=re.M|re.S)
        re_arranger = RegexStringArranger(expression)
        string='__test'
        dup_str=list(re_arranger.get_dup_str(string))
        de_dup_str=re_arranger.remove_dup_chars(string,dup_str)
        self.assertEqual(['_test'],de_dup_str) 

    def test_remove_dup_chars_end(self):
        expression = re.compile(r"(\-|\_|\ |\.)\1+",flags=re.M|re.S)
        re_arranger = RegexStringArranger(expression)
        string='test__'
        dup_str=list(re_arranger.get_dup_str(string))
        de_dup_str=re_arranger.remove_dup_chars(string,dup_str)
        self.assertEqual(['test_'],de_dup_str) 

    
if __name__ == '__main__':
    unittest.main()