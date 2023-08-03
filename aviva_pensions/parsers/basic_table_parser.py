from aviva_pensions.parsers.table_parser_interface import TableParserInterface
from aviva_pensions.parsers.name_parser import NameParser

class BasicTableParser(TableParserInterface):
    
    def __init__(self, name_parser:NameParser) -> None:
        super().__init__()
        self._data = {}
        self._name_parser = name_parser
        
    def get_name(self) -> str:
        return 'basic'
    
    def get_values(self) -> dict:
        return self._data
    
    def read_table(self, num, table) -> None:
        
        data = {}
            
        for row in table:
            
            # each row should have only 1 cell
            # split cells, use last word as the value 
            if len(row) == 1:
                
                cell = row[0].split()
                label = ' '.join(cell[:-1])
                
                label = self._name_parser.parse_label(label)
                
                if label != '':
                    try:
                        data[label] = cell[-1]
                    except IndexError:
                        data[label] = ''
                    
        self._data = self._data | data 
