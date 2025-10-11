import unittest

from content_download.parsers.url_parser import URLParser

class URLParserTest(unittest.TestCase):

    def test_parse(self):

        scheme_domain  = 'http://www.test.com'
        fixtures = self.get_fixtures()

        for fixture in fixtures:
            url_parser = URLParser(scheme_domain=scheme_domain)
            parsed_count = 0
            for url in url_parser.parse(fixture['html']):
                parsed_count += 1
                print(url)

            self.assertEqual(parsed_count, fixture['count'])


    def get_fixtures(self):

        return [

            {
                'html': '',
                'count': 0
            }
        ]