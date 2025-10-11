import unittest

from aviva_pensions.parsers.risks_parser import RisksParser

class RisksParserTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._names = ["General",
            "Cash/Money Market Funds",
            "Reinsured Funds"
        ]

        self._parser = RisksParser(self._names)

    def test_parse_risks(self) -> None:

        for test_name in self._names:

            text = '{}Yes'.format(test_name)
            results = self._parser.get_values(text=text)

            for other_name in self._names:
                if other_name != test_name:
                    self.assertTrue('No', results[other_name])
                else:
                    self.assertTrue('Yes', results[other_name])
