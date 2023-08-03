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
        
        # print("read_table: num {}".format(num))
        
        data = {}
        row_num = 0
            
        for row in table:
            # print(row)
            row_num += 1
            # print("read_table : row.num {} row.len {}".format(row_num, len(row)))
            
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
                    
                    # print("read_table : '{}'='{}'".format(label, data[label]))
            # elif len(row) == 2:
            #     data[row[0]] = row[1]
            #     print("read_table : '{}'='{}'".format(row[0], data[row[0]]))
                
        self._data = self._data | data 
