from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

from aviva_pensions.readers.data_provider_interface import DataProviderInterface


class AddColumnsPostProcessor(PostProcessorInterface):
    """
        Add columns from another csv to the report
    """

    def __init__(self, key:str, columns:list[str], data_provider:DataProviderInterface) -> None:
        self.__columns = columns
        self.__data_provider = data_provider
        self.__source_data = {}
        self.__key_name = key

    """
        add named columns from source csv to the data
        keyed on sedol
    """
    def process(self, row: dict) -> dict:

        if not len(self.__source_data):
            self.__source_data = self.__data_provider.read_data()

        # if the key is not in the input then add empty columns
        if not self.__key_name in row:
            print("key {} not found in {}".format(self.__key_name, row))
            for col in self.__columns:
                row[col] = ''
            return row

        # get the id to read from the data source
        id = str(row[self.__key_name])

        # remove leading 0s from the ids
        if key[0] == '0':
            key = str(int(key))

        if id in self.__source_data:

            source_data_row = self.__source_data[id]

            for col in self.__columns:
                if col in source_data_row:
                    if col in row:
                        if row[col] == '':
                            row[col] = source_data_row[col]
                    else:
                        row[col] = source_data_row[col]
                else:
                    row[col] = ''
        else:
            print("id {}\n not found in {}".format(id, self.__source_data.keys()))

        return row

    def _add_empty_cols(self, row:dict) -> dict:
        """ fill out the parameter dict with all the configured col names and empty values
        """
        for col in self._columns:
            row[col] = ''
        return row
