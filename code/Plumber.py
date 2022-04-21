
import re
from typing import Dict

from urllib3 import Retry


class Plumber:
    
    def __init__(self, file_name:str, pdf) -> None:
        self._file_name = file_name
        self._pdf = pdf
        self._data = {}
        # parse table data
        self._parseTables()
    
    @property
    def name(self)->str:
        return self._file_name
    
    @property
    def sedol(self)->str:
        if 'table_1' in self._data:
            if 'SSSSEEEEDDDDOOOOLLLL' in self._data['table_1']:
                return self._data['table_1']['SSSSEEEEDDDDOOOOLLLL']
        return ''
    
    @property
    def isin(self)->str:
        if 'table_3' in self._data:
            if 'IIIISSSSIIIINNNN CCCCooooddddeeee' in self._data['table_3']:
                return self._data['table_3']['IIIISSSSIIIINNNN CCCCooooddddeeee']
        return ''
    
    def _parseTables(self) -> None:
        page_1 = self._pdf.pages[0]
        page_1_tables = page_1.extract_tables(table_settings={})

        self._data['table_1'] = self._parseTable(page_1_tables[0])
        self._data['table_3'] = self._parseTable(page_1_tables[2])
        # if len(page_1_tables) > 3:
            # self._data['table_4'] = self._parseTable(page_1_tables[3])
        
        # print(self._data['table_1'])
        # print(self._data['table_3'])
        
    def _parseTable(self, table) -> Dict:
        
        data = {}        
        for row in table:
            # each row should have only 1 cell
            # split cells, use last word as the value 
            cell = row[0].split()
            label = ' '.join(cell[:-1])
            value = cell[-1]
            data[label] = value
        
        return data