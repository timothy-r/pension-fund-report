from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

from aviva_pensions.readers.data_provider_interface import DataProviderInterface


class AddColumnsPostProcessor(PostProcessorInterface):
    """
        Add columns from another csv to the report
    """

    def __init__(self, key:str, columns:list[str], data_provider:DataProviderInterface) -> None:
        self._key_name = key
        self._columns = {key: '' for key in columns}
        self._data_provider = data_provider
        self._source_data = {}

    def process(self, target_row: dict) -> dict:
        """
            add named columns from source csv to the data if they are not set
            add empty col values if the target_row key is not in the source data
            it might be clearer to generate a dict of values to add to target
            then use update to add those new values
        """
        if len(self._source_data) == 0:
            self._source_data = self._data_provider.read_data()

        try:
            key = self._get_key_value_from_target(target_row=target_row)
        except KeyError:
            key = None

        source_row = self._get_source_row(key=key, target_row=target_row)

        additions = self._calculate_additional_cols(target_row=target_row, source_row=source_row)

        target_row.update(additions)

        return target_row

    def _get_key_value_from_target(self, target_row:dict) -> str:
        # get the key value to read from the data source

        key = str(target_row[self._key_name])

        # remove leading 0s from the ids
        if key[0] == '0':
            key = str(int(key))

        return key

    def _get_source_row(self, key:str, target_row:dict) -> dict:
        """ Returns the source row data to add to the target
        """
        if not self._key_name in target_row:
            print("key {} not found in {}".format(self._key_name, target_row))
            # add empty columns
            return self._columns

        if key in self._source_data:
            # add columns from source
            return self._source_data[key]
        else:
            print("id {}\n not found in {}".format(key, self._source_data.keys()))
            # add empty columns
            return self._columns

    def _calculate_additional_cols(self, target_row:dict, source_row:dict) -> dict:
        """ generate a dict of keys & values to add to target from source
        """
        result = {}
        for col in self._columns:

            if col in source_row:
                # if the col exists but is empty then set the value
                if col in target_row and target_row[col] == '':
                    result[col] = source_row[col]
                elif not col in target_row:
                    # if the col does not exist in target then just set the value
                    result[col] = source_row[col]
            else:
                if not col in target_row:
                    result[col] = ''

        return result