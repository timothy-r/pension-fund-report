import unittest
from unittest.mock import Mock

from aviva_pensions.parsers.performance_table_parser import PerformanceTableParser

def makeFakeMethod():
    def fakeMethod(param):
        return param
    
    return fakeMethod

class PerformanceTableParserTest(unittest.TestCase):
    
    def test_read_table(self) -> None:
        
        header = ['', '30/06/18 To 30/06/19', '30/06/19 30/06/20','30/06/20 To 30/06/21','30/06/21 30/06/22','30/06/22 30/06/23']
        row_1 = ['Fund (%)', '2.27', '43.51','45.86', '-42.59', '16.90'] 
        row_2 = ['Bench- mark (%)', '9.48', '5.18','24.49', '-4.02', '11.14']
        table = []
        table.append(header)
        table.append(row_1)
        table.append(row_2)

        # simplify the test by getting the name parser to echo back its input
        name_parser = Mock()
        name_parser.parse_label = makeFakeMethod()
        
        perf_table_matrix_factory = Mock()
        
        perf_table_parser = PerformanceTableParser(
            name_parser=name_parser, 
            perf_matrix_parser_factory=perf_table_matrix_factory
        )
        
        perf_table_parser.read_table(num=0, table=table)
        
        data = perf_table_parser.get_data()
        
        self.assertTrue('fund' in data)
        
        fund_row = data['fund']

        expected = [
            {'date':'30/06/19', 'value':2.27},
            {'date':'30/06/20','value': 43.51}, 
            {'date':'30/06/21','value':45.86},
            {'date':'30/06/22','value':-42.59},
            {'date':'30/06/23','value':16.9}
        ]
        
        found = False
        
        for expected_item in expected:
            for row_item in fund_row:
                if row_item['date'] == expected_item['date']:
                    found = True
                    self.assertEquals(row_item['value'], expected_item['value'])

        self.assertTrue(found)
        
        self.assertTrue('benchmark' in data)
        
        benchmark_row = data['benchmark']

        expected = [
            {'date':'30/06/19', 'value': 9.48},
            {'date':'30/06/20','value': 5.18}, 
            {'date':'30/06/21','value': 24.49},
            {'date':'30/06/22','value':-4.02},
            {'date':'30/06/23','value':11.14}
        ]
        
        found = False
        
        for expected_item in expected:
            for row_item in benchmark_row:
                if row_item['date'] == expected_item['date']:
                    found = True
                    self.assertEquals(row_item['value'], expected_item['value'])

        self.assertTrue(found)