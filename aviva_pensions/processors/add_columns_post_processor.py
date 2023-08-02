import csv

from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

"""
    Add columns from another csv to the report
    Support falling back to a different key or fix the SEDOL lookup?
"""
class AddColumnsPostProcessor(PostProcessorInterface):
    
    def __init__(self, key:str, columns:list[str], reader) -> None:
        self._columns = columns
        self._reader = reader
        self._source_data = {}
        self._key_name = key
        
    """
        add named columns from source csv to the data
        keyed on sedol
    """
    def process(self, row: dict) -> dict:
        
        if not len(self._source_data):
            self._read_data()
        
        # if the key is not in the input then add empty columns        
        if not self._key_name in row:
            print("key {} not found in {}".format(self._key_name, row))
            for col in self._columns:
                row[col] = ''
            return row
        
        # get the id to read from the data source 
        id = str(row[self._key_name])
        
        if id in self._source_data:
            
            data_row = self._source_data[id]
            
            for col in self._columns:
                if col in data_row:
                    row[col] = data_row[col]
                else:
                    row[col] = ''
        else:
            print("id {} not found in {}".format(id, row))
            
        return row
    
    def _read_data(self):
        
        self._source_data = {}
        
        for row in self._reader:
            if self._key_name in row:
                self._source_data[str(row[self._key_name])] = row
            else:
                print(row)
            