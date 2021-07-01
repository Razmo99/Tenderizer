from app_tk_widgets import FileNamer
import re
import unittest
class TestFileNamer(unittest.TestCase):

    """
    Goals of this class

    * Generate a file name based on a prefix, regex match and suffix
     * Match groups can be selected and arranged
    * Remove duplicate deliminators and set them to all be the same
    * Clean illegal characters from the file name
     * These characters are changed to the specified deliminator

    Produced information
    * new file name in string format

    Dependancies
    * None

    """

    def setUp(self):
        self.file_namer = FileNamer(
            re.compile(r'(\-|\_|\ |\.)+',flags=re.S|re.M),
            re.compile(r'[\/\\\|\<\>\?\"\*\:\,]+',flags=re.S|re.M))
        self.prefix='DWG-XXX-XXX(6)'
        self.string0='Drawing Title\nServices - Lighting and Controls Level 6\n\nScale at A1'
        self.str_w_illegal_chars='Drawing Title\nServices - East\West <North> *Level 6\n\nScale at A1'
        self.string2='Drawing Title\nServices - Lighting and Controls Level 6\n\nScale at A1'
        self.str_newlines='Drawing Title\nServices - \n\nLighting and\n\n Controls Level 6\n\nScale at A1'
        self.str_multiple_match_groups='Drawing Title\nServices - \n\nLighting and\n\n Controls Level 6\n\nScale at A1\n\nRev\n\n05'
        self.suffix='.pdf'

    def test_dedup(self):
        fn=self.file_namer
        match=re.search(
            r'Drawing Title(.*)Scale',
            self.string0,
            flags=re.M|re.S)
        fn.deliminator='_'
        fn.match_order=[1]
        name=fn.new_file_name(
            self.prefix,
            self.suffix,
            match
        )
        self.assertEqual(
            name,
            'DWG_XXX_XXX(6)_Services_Lighting_and_Controls_Level_6.pdf'
        )
    
    def test_clean(self):
        fn=self.file_namer
        match=re.search(
            r'Drawing Title(.*)Scale',
            self.str_w_illegal_chars,
            flags=re.M|re.S)
        fn.deliminator=' '
        fn.match_order=[1]
        name=fn.new_file_name(
            self.prefix,
            self.suffix,
            match
        )
        self.assertEqual(name,'DWG XXX XXX(6) Services East West  North   Level 6.pdf')
    
    def test_match_order(self):     
        fn=self.file_namer
        match=re.search(
            r'Drawing Title(.*)Scale at A1.*?(Rev).*?(\d+)',
            self.str_multiple_match_groups,
            flags=re.M|re.S)
        fn.deliminator=' '
        fn.match_order=[1,2,3]
        name=fn.new_file_name(self.prefix,self.suffix,match)
        self.assertEqual(name,'DWG XXX XXX(6) Services Lighting and Controls Level 6 Rev 05.pdf')
        fn.match_order=[1,3,2]
        fn.deliminator='.'
        name=fn.new_file_name(self.prefix,self.suffix,match)
        self.assertEqual(name,'DWG.XXX.XXX(6).Services.Lighting.and.Controls.Level.6.05.Rev.pdf')
    
    def test_removes_newline(self):
        fn=self.file_namer
        match=re.search(
            r'Drawing Title(.*)Scale',
            self.str_newlines,
            flags=re.M|re.S)
        fn.deliminator='-'
        fn.match_order=[1]
        name=fn.new_file_name(self.prefix,self.suffix,match)
        self.assertEqual(name,'DWG-XXX-XXX(6)-Services-Lighting-and-Controls-Level-6.pdf')