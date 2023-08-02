import re

from aviva_pensions.processors.post_processor_interface import PostProcessorInterface
from aviva_pensions.parsers.name_parser import NameParser

"""
    insert prices into the data, if not already set
"""
class AddPricesChargesPostProcessor(PostProcessorInterface):
    
    def __init__(self, key:str, columns:list[str], reader, name_parser:NameParser) -> None:
        super().__init__()
        self._key_name = key
        self._columns = columns
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
            
            data_row = self._source_data[id]
            
            for col in self._columns:
                
                if col in data_row:
                
                    # don't overwrite cols with values
                    if col in row:
                        if row[col] == '':
                            row[col] = data_row[col]
                    else:
                        row[col] = data_row[col]
                
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
            
            
            