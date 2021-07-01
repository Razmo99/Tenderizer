from pathlib import PurePath
from dataclasses import dataclass
import re

@dataclass
class Pdf():
    """Class for Keeping track of all Pdf's being renamed"""
    name: str
    input_path: PurePath
    relative_output_path: PurePath
    output_path: PurePath
    converted: bool
    id: str
    text_data: str
    regex_matches: re.Match
    regex_match_group: int
    new_name: str
    rename_op: tuple

    def __init__(self,id,name,input_path):
        self.id=id
        self.name=name
        self.input_path=input_path
        self.converted=False

    def __repr__(self):
        return self.name