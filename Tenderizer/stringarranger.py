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