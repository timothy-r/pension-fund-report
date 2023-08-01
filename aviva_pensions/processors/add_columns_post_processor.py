import csv

from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

class AddColumnsPostProcessor(PostProcessorInterface):
    
    def __init__(self, columns:list[str], file:str) -> None:
        self._columns = columns
        self._file = file
        self._data = {}
        self._key = 'SEDOL'
        
    """
        add named columns from source csv to the data
        keyed on sedol
    """
    def process(self, data: dict) -> dict:
        
        if not len(self._data):
            self._read_data()
        
        # if the key is not in the input then add empty columns        
        if not self._key in data:
            for col in self._columns:
                data[col] = ''
            return data
        
        # get the key to read from the data source 
        key = data[self._key]
        
        if key in self._data:
            
            row = self._data[key]
            
            for col in self._columns:
                if col in row:
                    data[col] = row[col]
                else:
                    data[col] = ''
        
        return data
    
    def _read_data(self):
        self._data = {}
        with open(self._file) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if self._key in row:
                    self._data[row[self._key]] = row 
            