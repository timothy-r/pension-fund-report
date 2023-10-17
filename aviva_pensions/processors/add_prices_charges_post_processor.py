from aviva_pensions.processors.post_processor_interface import PostProcessorInterface
from aviva_pensions.readers.data_provider_interface import DataProviderInterface

"""
    insert prices into the data, if not already set
"""
class AddPricesChargesPostProcessor(PostProcessorInterface):

    def __init__(self, key:str, columns:list[str], data_provider:DataProviderInterface) -> None:
        super().__init__()
        self._key_name = key
        self._columns = columns
        self._data_provider = data_provider
        self._source_data = {}

    """
        similar to add_columns post processor
        can both classes be refactored to be the same?
    """
    def process(self, target_row: dict) -> dict:

        if len(self._source_data) == 0:
            self._source_data = self._data_provider.read_data()

        if not self._key_name in target_row:
            print("key {} not found in {}".format(self._key_name, target_row))
            for col in self._columns:
                if not col in target_row:
                    target_row[col] = ''
            return target_row

        key = str(target_row[self._key_name])

        if key in self._source_data:

            data_row = self._source_data[key]

            for col in self._columns:

                if col in data_row:

                    # don't overwrite cols with values
                    if col in target_row:
                        if target_row[col] == '':
                            target_row[col] = data_row[col]
                    else:
                        target_row[col] = data_row[col]

        else:
            print("id '{}' not found in source data".format(key))

        return target_row
