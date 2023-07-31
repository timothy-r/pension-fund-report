from aviva_pensions.parsers.table_parser_interface import TableParserInterface

class BasicTableParser(TableParserInterface):
    
    def __init__(self) -> None:
        super().__init__()
        self._data = {}
        
    def get_name(self) -> str:
        return 'basic'
    
    def get_values(self) -> dict:
        return self._data
    
    def read_table(self, table) -> None:
        
        data = {}        
        for row in table:
            # print(row)

            # each row should have only 1 cell
            # split cells, use last word as the value 
            if len(row) == 1:
                cell = row[0].split()
                label = ' '.join(cell[:-1])
                
                label = self._fix_duplicate_characters(label)
                try:
                    data[label] = cell[-1]
                except IndexError:
                    data[label] = ''
                    
            elif len(row) == 2:
                data[row[0]] = row[1]
        
        self._data = self._data | data 
    
    # convert to a table_label_extractor?
    
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