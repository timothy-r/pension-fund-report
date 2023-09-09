from aviva_pensions.parsers.table_parser_interface import TableParserInterface
from aviva_pensions.parsers.name_parser import NameParser

class BasicTableParser(TableParserInterface):
    
    def __init__(self, name_parser:NameParser) -> None:
        super().__init__()
        self.__data = {}
        self.__name_parser = name_parser
        
    def get_name(self) -> str:
        return 'basic'
    
    def get_values(self) -> dict:
        return self.__data
    
    def read_table(self, num, table) -> None:
        
        data = {}
            
        for row in table:
            
            # each row should have only 1 cell
            # split cells, use last word as the value 
            if len(row) == 1:
                
                cell = row[0].split()
                label = ' '.join(cell[:-1])
                
                label = self.__name_parser.parse_label(label)
                
                if label != '':
                    try:
                        data[label] = cell[-1]
                    except IndexError:
                        data[label] = ''
                    
        self.__data = self.__data | data 
