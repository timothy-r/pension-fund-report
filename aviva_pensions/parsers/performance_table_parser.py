from aviva_pensions.parsers.table_parser_interface import TableParserInterface
from aviva_pensions.parsers.performance_matrix import PerformanceMatrix

class PerformanceTableParser(TableParserInterface):
    
    def __init__(self, table_cell_label_parser) -> None:
        super().__init__()
        self._data = {}
        self._table_cell_label_parser = table_cell_label_parser
        
    def get_name(self) -> str:
        return 'performance'
    
    def get_values(self) -> dict:
        # print(self._data)
        return { self.get_name() : PerformanceMatrix(self._data) }
    
    def read_table(self, num, table) -> None:
        # return a dict of dicts
        row_num = 0
        
        header = []
        
        # first row is the column headers, first cell in first row is empty
        for row in table:
            row_num += 1
            
            if len(row) == 6:
                row_dict = {}
                
                if row_num == 1:
                    header = self._parse_table_header(row)
                    # print(header)
                else:
                    cell = row[0].split()
                    label = ' '.join(cell)
                    label = self._table_cell_label_parser.parse_label(label)
                    
                    # print("label : {}".format(label))
                    index = 0
                    for c in row:
                        # print("cell :{} {}".format(index, c))
                        if index > 0 and index < len(header):
                            row_dict[header[index]] = c
                        index += 1
                        
                    self._data[label] = row_dict
                
                # print(row_dict)
                
    def _parse_table_header(self, row):
        data = []
        for cell in row:
            raw = cell.split()
            label = ' '.join(raw)
            value = self._table_cell_label_parser.parse_label(label)
            data.append(value)

        return data