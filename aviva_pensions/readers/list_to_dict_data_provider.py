from typing import Iterable

from aviva_pensions.readers.data_provider_interface import DataProviderInterface

class ListToDictDataProvider(DataProviderInterface):
    """ Convert a list of dicts into a dict using one of the keys
    """
    def __init__(self, key:str, reader:Iterable) -> None:
        self._key_name = key
        self._reader = reader

    def read_data(self) -> dict:
        """Read the data from source, map into the result dict"""
        data = {}

        for row in self._reader:

            if self._key_name in row:
                data[str(row[self._key_name])] = row
            else:
                print("_read_data error, key {} not found in {}".format(self._key_name, row))

        return data
