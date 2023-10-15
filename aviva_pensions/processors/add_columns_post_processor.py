from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

from aviva_pensions.readers.data_provider_interface import DataProviderInterface

"""
    Add columns from another csv to the report
"""
class AddColumnsPostProcessor(PostProcessorInterface):

    def __init__(self, key:str, columns:list[str], data_provider:DataProviderInterface) -> None:
        self._columns = columns
        self._data_provider = data_provider
        self._source_data = {}
        self._key_name = key

    """
        add named columns from source csv to the data
        keyed on sedol
    """
    def process(self, row: dict) -> dict:

        if not len(self._source_data):
            self._source_data = self._data_provider.read_data()

        # if the key is not in the input then add empty columns
        if not self._key_name in row:
            print("key {} not found in {}".format(self._key_name, row))
            for col in self._columns:
                row[col] = ''
            return row

        # get the id to read from the data source
        id = str(row[self._key_name])

        # remove leading 0s from the ids
        if id[0] == '0':
            id = str(int(id))

        if id in self._source_data:

            source_data_row = self._source_data[id]

            for col in self._columns:
                if col in source_data_row:
                    if col in row and row[col] == '':
                        row[col] = source_data_row[col]
                else:
                    row[col] = ''
        else:
            print("id {}\n not found in {}".format(id, self._source_data.keys()))

        return row