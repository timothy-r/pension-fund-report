from aviva_pensions.parsers.name_parser import NameParser
from aviva_pensions.parsers.char_stream_parser_interface import CharStreamParserInterface
from aviva_pensions.parsers.text_parser_interface import TextParserInterface
from aviva_pensions.parsers.table_parser_interface import TableParserInterface

"""
    Orchestrates reading data from a PDF
    Calls its configured parsers to read the data
"""
class PDFReader:
    
    def __init__(
        self, 
        char_stream_parsers:list[CharStreamParserInterface], 
        text_parsers:list[TextParserInterface],
        table_parsers: list[TableParserInterface],
        file_name_parser: NameParser
    ) -> None:
        
        self.__char_stream_parsers = char_stream_parsers
        self.__text_parsers = text_parsers
        self.__table_parsers = table_parsers
        self.__file_name_parser = file_name_parser
        self.__num_tables = 0
        
    """ 
        class to extract table data as key values from PDF pages
    """    
    def read(self, file_name:str, pdf) -> None:
        
        self.__file_name = file_name.name
        self.__pdf = pdf
        self.__text = ''
        self.__num_tables = 0
        
        # parse table data
        self.__parse_pages()
    
    def get_data(self):
        
        results = { 
            "Name": self.__file_name_parser.parse_file_name(self.__file_name),
            "FileName": self.__file_name
        }
        
        for parser in self.__table_parsers:
            results |= parser.get_values()
        
        for parser in self.__char_stream_parsers:
            results |= parser.get_values()
        
        for parser in self.__text_parsers:
            results |= parser.get_values(self.__text)
            
        return results
    
    def __parse_pages(self) -> None:
        total_pages = len(self.__pdf.pages)
        
        for p in range(0, total_pages-1):
            
            page = self.__pdf.pages[p]
            
            self.__parse_page_tables(page)
            self.__text += self.__parse_page_text(page)
            
    def __parse_page_text(self, page) -> None:
        text = []
        for char in page.chars:
            text.append(char['text'])

            for parser in self.__char_stream_parsers:
                parser.add_char(char=char)
        
        return ''.join(text)
        
            
    def __parse_page_tables(self, page) -> None:
        
        page_tables = page.extract_tables(
            table_settings = { } 
        )
        
        total_tables = len(page_tables)
        
        for t in range(0, total_tables-1):
            
            self.__num_tables += 1
            
            for parser in self.__table_parsers:
                parser.read_table(self.__num_tables, page_tables[t])
