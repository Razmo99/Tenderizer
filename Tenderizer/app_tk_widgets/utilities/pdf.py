from pathlib import PurePath, Path
from dataclasses import dataclass
import re

@dataclass
class Pdf():
    """Class for Keeping track of all Pdf's being renamed"""
    name: str
    input_path: PurePath
    input_dir: PurePath
    output_path: PurePath
    output_dir: PurePath
    id: str
    text_data: str
    regex_matches: re.Match
    regex_match_group: int
    rename_op: tuple
    converted: bool = False
    new_name: str = ''

    def __init__(self,input_path:PurePath,id='0') -> None:
        self.id=id
        self.input_path=PurePath(input_path)
        self.name=self.input_path.name

    def __repr__(self) -> str:
        return self.name

    def get_rename_path(self) -> PurePath:
        return self.input_dir / self.new_name

    def get_rename_path_len(self) -> int:
        return len(self.get_rename_path().__str__())

    def set_output_path(self,suffix='.txt') -> None:
        self.output_path=self.output_dir.joinpath(self.get_input_path_rel_dir()).with_suffix(suffix)

    def get_input_path_rel_dir(self) -> PurePath:
        return self.input_path.relative_to(self.input_dir)
    
    def get_output_path_rel_dir(self) -> PurePath:
        return self.output_path.relative_to(self.output)
