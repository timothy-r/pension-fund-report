# from typing import Dict
from aviva_pensions.parsers.file_name_parser import FileNameParser


class Plumber:
    
    def __init__(
        self, 
        char_stream_parsers:list, 
        text_parsers:list,
        table_parsers: list,
        file_name_parser: FileNameParser
    ) -> None:
        
        self._char_stream_parsers = char_stream_parsers
        self._text_parsers = text_parsers
        self._table_parsers = table_parsers
        self._file_name_parser = file_name_parser
        
    """ 
        class to extract table data as key values from PDF pages
    """    
    def read(self, file_name:str, pdf) -> None:
        self._file_name = file_name.name
        self._pdf = pdf
        self._text = ''
        
        # parse table data
        self._parsePages()
    
    def get_data(self):
        
        results = { "Name": self._file_name_parser.parse_name(self._file_name)}
        
        for parser in self._table_parsers:
            results |= parser.get_values()
        
        for parser in self._char_stream_parsers:
            results[parser.get_name()] = parser.get_value()
        
        for parser in self._text_parsers:
            results |= parser.get_value(self._text)
            
        return results
    
    def _parsePages(self) -> None:
        total_pages = len(self._pdf.pages)
        # print("pages: {}".format(total_pages))
        
        for p in range(0, total_pages-1):
            # print("page: {}".format(p))
            
            page = self._pdf.pages[p]
            
            self._parsePageTables(page)
            self._text += self._parsePageText(page)
            
    def _parsePageText(self, page) -> None:
        text = []
        for char in page.chars:
            text.append(char['text'])
            # extract risk number
            for parser in self._char_stream_parsers:
                parser.add_char(char=char)
        
        return ''.join(text)
        
            
    def _parsePageTables(self, page) -> None:
        
        page_tables = page.extract_tables(
            table_settings = { } 
        )
        
        total_tables = len(page_tables)
        # print("tables: {}".format(total_tables))
        
        for t in range(0, total_tables-1):
            # for table in [0,1,2]:
            # print("table: {}".format(t))
            for parser in self._table_parsers:
                parser.read_table(page_tables[t])
