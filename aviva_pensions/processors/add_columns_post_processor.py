from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

from aviva_pensions.readers.data_provider_interface import DataProviderInterface


class AddColumnsPostProcessor(PostProcessorInterface):
    """
        Add columns from another csv to the report
    """

    def __init__(self, key:str, columns:list[str], data_provider:DataProviderInterface) -> None:
        self._columns = columns
        self._data_provider = data_provider
        self._source_data = {}
        self._key_name = key


    def process(self, row: dict) -> dict:
        """
            add named columns from source csv to the data
            keyed on sedol
        """
        if len(self._source_data) == 0:
            self._source_data = self._data_provider.read_data()

        # if the key is not in the input then add empty columns
        if not self._key_name in row:
            print("key {} not found in {}".format(self._key_name, row))
            row = self._add_empty_cols(row=row)
            return row

        # get the id to read from the data source
        key = str(row[self._key_name])

        # remove leading 0s from the ids
        if key[0] == '0':
            key = str(int(key))

        if key in self._source_data:

            source_data_row = self._source_data[key]

            for col in self._columns:
                if col in source_data_row:
                    if col in row and row[col] == '':
                        row[col] = source_data_row[col]
                    else:
                        row[col] = source_data_row[col]
                else:
                    row[col] = ''
        else:
            row = self._add_empty_cols(row=row)
            print("id {}\n not found in {}".format(key, self._source_data.keys()))

        return row

    def _add_empty_cols(self, row:dict) -> dict:
        """ fill out the parameter dict with all the configured col names and empty values
        """
        for col in self._columns:
                row[col] = ''
        return row
