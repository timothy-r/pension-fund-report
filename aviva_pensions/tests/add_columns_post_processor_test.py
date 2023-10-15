import unittest

from aviva_pensions.processors.add_columns_post_processor import AddColumnsPostProcessor
from aviva_pensions.readers.list_to_dict_data_provider import ListToDictDataProvider

class AddColumnsPostProcessorTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_add_cols(self) -> None:
        key = 'SEDOL'
        cols = ['Charge','MS ratings', 'FT ratings']
        data = [
            {'SEDOL':'B5M9Z37', 'Charge':'0.17%', 'MS ratings':'4', 'FT ratings':'3'},
            {'SEDOL':'B7M1101', 'Charge':'0.20%', 'MS ratings':'5', 'FT ratings':'2'}
        ]

        data_provider = ListToDictDataProvider(key=key, reader=data)
        _processor = AddColumnsPostProcessor(key=key, columns=cols,data_provider=data_provider)

        row = {'SEDOL':'B5M9Z37'}
        results = _processor.process(row=row)

        self.assertTrue(4 == len(results))
        self.assertTrue('B5M9Z37' == results['SEDOL'])
        self.assertTrue('0.17%' == results['Charge'])
        self.assertTrue('4' == results['MS ratings'])
        self.assertTrue('3' == results['FT ratings'])

    def test_add_cols_with_numeric_key(self) -> None:
        key = 'SEDOL'
        cols = ['Charge','MS ratings', 'FT ratings']
        data = [
            {'SEDOL':3346251, 'Charge':'0.17%', 'MS ratings':'4', 'FT ratings':'3'},
            {'SEDOL':'3349036', 'Charge':'0.20%', 'MS ratings':'5', 'FT ratings':'2'}
        ]

        data_provider = ListToDictDataProvider(key=key, reader=data)

        _processor = AddColumnsPostProcessor(key=key, columns=cols,data_provider=data_provider)

        row = {'SEDOL':'03346251'}
        results = _processor.process(row=row)

        self.assertTrue(4 == len(results))
        self.assertTrue('03346251' == results['SEDOL'])
        self.assertTrue('0.17%' == results['Charge'])
        self.assertTrue('4' == results['MS ratings'])
        self.assertTrue('3' == results['FT ratings'])

    def test_add_empty_cols(self):
        key = 'SEDOL'
        cols = ['Charge','MS ratings', 'FT ratings']
        data = [
            {'SEDOL':3346251, 'Charge':'0.17%', 'MS ratings':'4', 'FT ratings':'3'},
            {'SEDOL':'3349036', 'Charge':'0.20%', 'MS ratings':'5', 'FT ratings':'2'}
        ]

        data_provider = ListToDictDataProvider(key=key, reader=data)

        _processor = AddColumnsPostProcessor(key=key, columns=cols,data_provider=data_provider)

        row = {'SEDOL':'0123456'}
        results = _processor.process(row=row)

        self.assertTrue(4 == len(results))
        self.assertTrue('0123456' == results['SEDOL'])
        self.assertTrue('' == results['Charge'])
        self.assertTrue('' == results['MS ratings'])
        self.assertTrue('' == results['FT ratings'])