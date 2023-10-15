from aviva_pensions.parsers.name_parser import NameParser
from aviva_pensions.parsers.char_stream_parser_interface import CharStreamParserInterface
from aviva_pensions.parsers.text_parser_interface import TextParserInterface
from aviva_pensions.parsers.table_parser_interface import TableParserInterface


class Plumber:
    """
        Orchestrates reading data from a PDF
        Calls its configured parsers to read the data
    """
    def __init__(
        self,
        char_stream_parsers:list[CharStreamParserInterface],
        text_parsers:list[TextParserInterface],
        table_parsers: list[TableParserInterface],
        file_name_parser: NameParser
    ) -> None:

        self._char_stream_parsers = char_stream_parsers
        self._text_parsers = text_parsers
        self._table_parsers = table_parsers
        self._file_name_parser = file_name_parser
        self._num_tables = 0


    def read(self, file_name:str, pdf) -> None:
        """  class to extract table data as key values from PDF pages """
        self._file_name = file_name.name
        self._pdf = pdf
        self._text = ''
        self._num_tables = 0

        # parse table data
        self._parse_pages()

    def get_data(self):

        results = {
            "Name": self._file_name_parser.parse_file_name(self._file_name),
            "FileName": self._file_name
        }

        for parser in self._table_parsers:
            results |= parser.get_values()

        for parser in self._char_stream_parsers:
            results |= parser.get_values()

        for parser in self._text_parsers:
            results |= parser.get_values(self._text)

        return results

    def _parse_pages(self) -> None:
        total_pages = len(self._pdf.pages)
        # print("pages: {}".format(total_pages))

        for p in range(0, total_pages-1):
            # print("page: {}".format(p))

            page = self._pdf.pages[p]

            self._parse_page_tables(page)
            self._text += self._parse_page_text(page)

    def _parse_page_text(self, page) -> None:
        text = []
        for char in page.chars:
            text.append(char['text'])

            for parser in self._char_stream_parsers:
                parser.add_char(char=char)

        return ''.join(text)


    def _parse_page_tables(self, page) -> None:

        page_tables = page.extract_tables(
            table_settings = { }
        )

        total_tables = len(page_tables)
        # print("tables: {}".format(total_tables))

        for t in range(0, total_tables-1):
            # print("table: {}".format(page_tables[t]))

            self._num_tables += 1

            for parser in self._table_parsers:
                parser.read_table(self._num_tables, page_tables[t])
