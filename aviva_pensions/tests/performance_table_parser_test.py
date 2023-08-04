import unittest
from unittest.mock import Mock
from aviva_pensions.container import Container

from aviva_pensions.parsers.performance_table_parser import PerformanceTableParser
from aviva_pensions.parsers.performance_matrix import PerformanceMatrix

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

        container = Container()
        perf_table_parser = container.perf_table_parser()
        
        # simplify the test by getting the name parser to echo back its input
        name_parser = Mock()
        name_parser.parse_label = makeFakeMethod()
        perf_table_parser._name_parser = name_parser
        
        perf_table_parser.read_table(num=0, table=table)
        
        data = perf_table_parser.get_values()
        
        matrix:PerformanceMatrix =  data['performance']
        
        self.assertIsInstance(matrix, PerformanceMatrix)
        
        self.assertEquals(0.6, matrix.fund_to_benchmark_average())
        
        expected_annual_perf = {
            'Year': {
                'date': '30/06/23',
                'value':16.90
            }
        }
        
        actual_annual_perf = matrix.fund_annual_performance()
        self.assertEquals(expected_annual_perf["Year"], actual_annual_perf["Year"])