import re

from aviva_pensions.parsers.text_parser_interface import TextParserInterface

class ReportDateParser(TextParserInterface):

    def __init__(self) -> None:
        super().__init__()

    def get_name(self) -> str:
        return 'date'

    """
        Fund factsAs at 30/06/2023
    """
    def get_values(self, text: str) -> dict:

        match = re.search(r'Fund factsAs at ([0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4})', text)
        date = match.group(1)
        return {self.get_name(): date}