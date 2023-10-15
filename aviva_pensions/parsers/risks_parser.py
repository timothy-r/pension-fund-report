import re

from aviva_pensions.parsers.text_parser_interface import TextParserInterface

class RisksParser(TextParserInterface):

    def __init__(self, names:list[str]) -> None:
        super().__init__()

        self._risk_names = names

    def get_name(self) -> str:
        return 'risks'

    def get_values(self, text: str) -> dict:

        values = {}

        for name in self._risk_names:
            result = re.search("{}Yes".format(name), text)
            if result != None:
                values[name] = 'Yes'
            else:
                values[name] = 'No'

        return values
