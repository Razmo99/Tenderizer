class StringArranger():
    
    def get_duplicate_chars(self,string,dup_chars):
        str_len=len(string) - 1
        for index,char in enumerate(string):
            if char in dup_chars:
                ahead=index+1 if index < str_len else index
                if index < str_len and string[ahead] in dup_chars:
                    yield ahead