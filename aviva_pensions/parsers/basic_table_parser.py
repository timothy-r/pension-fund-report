from aviva_pensions.parsers.table_parser_interface import TableParserInterface

class BasicTableParser(TableParserInterface):
    
    def __init__(self, table_cell_label_parser) -> None:
        super().__init__()
        self._data = {}
        self._table_cell_label_parser = table_cell_label_parser
        
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
                
                label = self._table_cell_label_parser.parse_label(label)
                # label = self._fix_duplicate_characters(label)
                
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
    
    """ 
        fix duplicated characters in label - all non-space chars 
    """
    def _fix_duplicate_characters(self, value:str)-> str:
   
        words = value.split()
        result = []
        for word in words:
            # keep every 4th char
            chars = word[::4]
            result.append(''.join(chars))
        
        result = ' '.join(result)
        
        return result