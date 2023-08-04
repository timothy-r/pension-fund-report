from typing import Callable

from aviva_pensions.parsers.table_parser_interface import TableParserInterface
from aviva_pensions.parsers.performance_matrix import PerformanceMatrix
from aviva_pensions.parsers.performance_matrix_row import PerformanceMatrixRow
from aviva_pensions.parsers.name_parser import NameParser

class PerformanceTableParser(TableParserInterface):
    
    def __init__(
        self, 
        name_parser:NameParser, 
        perf_matrix_factory:Callable[..., PerformanceMatrix],
        perf_matrix_row_factory:Callable[..., PerformanceMatrixRow]
    ) -> None:
        
        super().__init__()
        
        # store each row in a PerformanceMatrix instance
        self._data = {}
        
        self._name_parser = name_parser
        self._perf_matrix = perf_matrix_factory()
        
        # self._perf_matrix_factory = perf_matrix_factory
        self._perf_matrix_row_factory = perf_matrix_row_factory
        
        self._data_keys = {
            'Fund (%)' : 'fund',
            'Bench- mark (%)' : 'benchmark',
            'Sector Average (%)' : 'sector_ave',
            'Quartile rank within sector': 'quart_rank_in_sector'
        }
        
    def get_name(self) -> str:
        return 'performance'
    
    def get_data(self) -> dict:
        return self._data
    
    def get_values(self) -> dict:
        return { self.get_name() :  self._perf_matrix}
    
    def read_table(self, num, table) -> None:
        # return a dict of dicts
        row_num = 0
        
        header = []
        
        # first row is the column headers, first cell in first row is empty
        for row in table:
            
            row_num += 1
            
            if len(row) == 6:
                
                if row_num == 1:
                    header = self._parse_table_header(row)
                else:
                    self._parse_table_row(header=header, row=row)
                
                
    def _parse_table_header(self, row) -> None:
        data = []
        for cell in row:
            raw = cell.split()
            label = ' '.join(raw)
            value = self._name_parser.parse_label(label)
            # spilt & use the last date in the label
            value = value.split(' ')[-1]
            data.append(value)

        return data

    def _parse_table_row(self, header:list, row) -> None:
        
        result = []
        
        # first item is the row label
        cell = row[0].split()
        label = ' '.join(cell)
        label = self._name_parser.parse_label(label)
        
        # map label from pdf to the internal label name
        if label in self._data_keys:
            label = self._data_keys[label]
        
        
        for i in range(1, len(header)):
            row_dict = {}
            row_dict['date'] = header[i]
            row_dict['value'] = float(row[i])
            result.append(row_dict)
            
        
        # create a PerformanceMatrixRow here
        
        self._perf_matrix.add_row(
            name=label,
            row=self._perf_matrix_row_factory(data=result)
        )