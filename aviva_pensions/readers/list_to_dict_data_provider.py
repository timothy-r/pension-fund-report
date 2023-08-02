from aviva_pensions.readers.data_provider_interface import DataProviderInterface

"""
    convert a list of dicts into a dict using one of the keys
"""
class ListToDictDataProvider(DataProviderInterface):
    
    def __init__(self, key:str, reader) -> None:
        self._key_name = key
        self._reader = reader
    
    def read_data(self) -> dict:
        data = {}
        
        for row in self._reader:
            
            if self._key_name in row:
                data[str(row[self._key_name])] = row
            else:
                print("_read_data error, key {} not found in {}".format(self._key_name, row))
        
        return data