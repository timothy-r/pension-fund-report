import unittest

from aviva_pensions.parsers.risk_parser import RiskParser

class RiskParserTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._parser = RiskParser()

    def test_parse_risk(self) -> None:
        risk = '1'
        chars = self.get_test_data(['1','2','3','4','5','6','7'], risk)
        for char in chars:
            self._parser.add_char(char=char)

        result = self._parser.get_values()
        self.assertEquals({'risk': risk}, result)

    def test_parse_risk_from_many_chars(self) -> None:
        risk = '3'
        chars = self.get_test_data(['a','b','1','2','3','4','5','6','7','G','H','0'], risk)
        for char in chars:
            self._parser.add_char(char=char)

        result = self._parser.get_values()
        self.assertEquals({'risk': risk}, result)

    def test_parse_risk_from_many_digits(self) -> None:
        risk = '7'
        chars = self.get_test_data(['1','1','2','3','4','5','6','7','11','1','0'], risk)
        for char in chars:
            self._parser.add_char(char=char)

        result = self._parser.get_values()
        self.assertEquals({'risk': risk}, result)

    def test_parse_risk_without_selecton(self) -> None:
        risk = '0'
        chars = self.get_test_data(['1','2','3','4','5','6','7'], risk)
        for char in chars:
            self._parser.add_char(char=char)

        result = self._parser.get_values()
        self.assertEquals({'risk': ''}, result)


    def get_test_data(self, chars:list, risk:str) -> list:

        data = []
        for char in chars:
            if risk == char:
                colour = (0,0,0)
            else:
                colour = (1,1,1)
            data.append(
                {
                    'text': char,
                    'stroking_color': colour,
                    'non_stroking_color': colour
                }
            )
        return data