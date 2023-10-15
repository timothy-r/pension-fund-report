import unittest

from aviva_pensions.parsers.name_parser import NameParser

class NameParserTest(unittest.TestCase):

    def test_parse_label(self) -> None:

        raw = [
            'SSSSEEEEDDDDOOOOLLLL',
            'FFFFuuuunnnndddd ((((%%%%))))',
            'BBBBeeeennnncccchhhh---- mmmmaaaarrrrkkkk ((((%%%%))))',
            '33330000////00006666////11118888 33330000////00006666////11119999'
            ]
        expected = [
            'SEDOL',
            'Fund (%)',
            'Bench- mark (%)',
            '30/06/18 30/06/19']

        parser = NameParser()

        for i in range(0, len(raw)):
            result = parser.parse_label(raw[i])
            self.assertEquals(expected[i], result)

