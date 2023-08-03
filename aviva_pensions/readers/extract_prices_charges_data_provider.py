import re
from typing import Iterable

from aviva_pensions.readers.data_provider_interface import DataProviderInterface
from aviva_pensions.parsers.name_parser import NameParser


class ExtractPricesChargesDataProvider(DataProviderInterface):
    
    def __init__(self, reader:Iterable, name_parser:NameParser) -> None:
        self._reader = reader
        self._name_parser = name_parser
    
    def read_data(self) -> dict:
        data = {}
        
        # remove leading Av and trailing FP
        for row in self._reader:
            # spilt first column into name & charge
            fund_name = row['Fund name']
            match = re.search(r'([^(]+)[(](([^)]+))', fund_name)
            name = self._name_parser.parse_fund_name(match.group(1))
            charge = match.group(2).split(' ')[0]
            
            data[name] = {'Charge': charge, 'Price': row['Unit prices']}

        return data