import logging
import re

logger = logging.getLogger(__name__)


class FileNamer():
    """ Class to facilitate renaming files"""

    def __init__(self, de_dup_regexp, clean_regexp):
        self.de_dup_regexp = de_dup_regexp
        self.clean_regexp = clean_regexp
        self.newline_regexp = re.compile(r"[\r\n|\n|\r]+", flags=re.M | re.S)
        self.match_order = []
        self.deliminator = '_'

    def clear_illegal_char(self, string):
        """ clears characters targeted by the specified regex on class init, replaced with selected deliminator """
        return re.sub(self.clean_regexp, self.deliminator, string)

    def remove_newline(self, string):
        """ Removes newline chars \n \r \r\n """
        return re.sub(self.newline_regexp, '', string)

    def set_match_deliminator(self, string_array):
        """ Takes in an array of strings,
            changes the deliminator to whats set in this class.
            deliminators are changed based on the regex in de_dup_regexp.
        """
        results = string_array.copy()
        for index, string in enumerate(results):
            s = string.strip() if len(string) > 1 else string
            results[index] = re.sub(self.de_dup_regexp, self.deliminator, self.remove_newline(s))
        return results

    def new_file_name(self, prefix, suffix, matches):
        """ Generates a file name based on selection order and deliminator """
        file_name = self._initialize_file_name(matches)

        if file_name:
            file_name.insert(0, self.deliminator)
            file_name.insert(0, prefix)
            # remove the tail deliminator
            del file_name[-1]
            adjusted_deliminators = self.set_match_deliminator(file_name)
            adjusted_deliminators.append(suffix)
            result = ''.join(adjusted_deliminators)
            return self.clear_illegal_char(result)

    def _initialize_file_name(self, matches):
        """ Initialize the core file name based on regex results"""
        results = []
        for match_id in self.match_order:
            try:
                match = matches.group(match_id)
            except IndexError:
                logger.debug(f'Failed to find match order:{match_id}')
            else:
                results.append(match)
                results.append(self.deliminator)
        return results
