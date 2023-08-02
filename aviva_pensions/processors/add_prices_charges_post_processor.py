import re

from aviva_pensions.processors.post_processor_interface import PostProcessorInterface
from aviva_pensions.parsers.name_parser import NameParser

"""
    insert prices into the data, if not already set?
"""
class AddPricesChargesPostProcessor(PostProcessorInterface):
    
    def __init__(self, reader, name_parser:NameParser) -> None:
        super().__init__()
        # self._keys = keys
        self._key_name = 'Name'
        self._cols = ['Charge', 'Price']
        self._reader = reader
        self._name_parser = name_parser
        self._source_data = {}
    
    """
        similar to add_columns post processor
        can both classes be refactored to be the same?
    """
    def process(self, row: dict) -> dict:
        
        if not len(self._source_data):
            self._read_data()
        
        if not self._key_name in row:
            print("key {} not found in {}".format(self._key_name, row))
            for col in self._columns:
                if not col in row:
                    row[col] = ''
            return row
        
        id = str(row[self._key_name])
        if id in self._source_data:
            for k in self._source_data[id].keys():
                # don't overwrite cols with values
                if k in row:
                    if row[k] == '':
                        row[k] = self._source_data[id][k]
                else:
                    row[k] = self._source_data[id][k]
            
        else:
            print("id '{}' not found in source data".format(id))
        
        return row
    
    def _read_data(self):
        self._source_data = {}
        
        # remove leading Av and trailing FP
        for row in self._reader:
            # spilt first column into name & charge
            fund_name = row['Fund name']
            match = re.search(r'([^(]+)[(](([^)]+))', fund_name)
            name = self._name_parser.parse_fund_name(match.group(1))
            charge = match.group(2).split(' ')[0]
            
            self._source_data[name] = {'Charge': charge, 'Price': row['Unit prices']}
            
            
            