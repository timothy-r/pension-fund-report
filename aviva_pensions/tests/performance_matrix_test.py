import unittest

from aviva_pensions.container import Container

from aviva_pensions.parsers.performance_matrix import PerformanceMatrix
from aviva_pensions.tests.test_data_provider import TestDataProvider
class PerformanceMatrixTest(unittest.TestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self._container = Container()
        
        # some data has the word To between the 2 dates
        self._cols = ['30/06/18 To 30/06/19', '30/06/19 30/06/20', '30/06/20 To 30/06/21', '30/06/21 30/06/22', '30/06/22 30/06/23']
        self._matrix_cols = ["Year", "Year-1", "Year-2", "Year-3", "Year-4"]
        self._test_data_provider = TestDataProvider()
        
    def test_fund_to_benchmark_average_fund_higher(self):
        
        matrix = self._get_test_matrix({
            'fund': [12.94, 9.62,19.01,5.91,8.77],
            'benchmark': [10.05, 4.12,1.99,3.01,1.03]
        })
        
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(1, result)
    
    def test_fund_to_benchmark_average_fund_lower(self):
        matrix = self._get_test_matrix({
            'fund': [10.05, 4.12,1.99,3.01,1.03],
            'benchmark':[12.94, 9.62,19.01,5.91,8.77]
        })
        
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(0, result)
    
    def test_fund_to_benchmark_average_fund_60_percent(self):
        matrix = self._get_test_matrix({
            'fund': [10.05, 4.12,17.99,9.01,1.03],
            'benchmark':[12.94, 1.62,11.01,5.91,8.77]
        })
        
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(0.6, result)
    
    def test_fund_to_benchmark_average_fund_validates_data(self):
        matrix = self._get_test_matrix({})
        
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(None, result)
    
    def xtest_fund_to_benchmark_average_handles_strings(self):
        matrix = self._get_test_matrix({
            'fund': ['-', 14.12,1.99,3.01,'_'],
            'benchmark': [12.94, '-',19.01,5.91,'/']
        })
        
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(0, result)
        
    def test_fund_to_sector_average_validates_data(self):
        matrix = self._get_test_matrix({})
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(None, result)

    def test_fund_to_sector_average_fund_higher(self):
        matrix = self._get_test_matrix({
            'fund': [12.94, 9.62,19.01,5.91,8.77],
            'sector': [10.05, 4.12,1.99,3.01,1.03]
        })
        
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(1, result)

    def test_fund_to_sector_average_fund_lower(self):
        matrix = self._get_test_matrix({
            'fund': [10.05, 4.12,1.99,3.01,1.03],
            'sector': [12.94, 9.62,19.01,5.91,8.77]
        })
        
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(0, result)

    def test_fund_to_sector_average_fund_20_percent(self):
        matrix = self._get_test_matrix({
            'fund': [10.0, 14.0, 1.0, 3.0, 1.0],
            'sector': [12.0, 9.0, 19.0, 5.0, 8.0]
        })
        
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(0.2, result)

    def xtest_fund_to_sector_average_handles_strings(self):
        matrix = self._get_test_matrix({
            'fund': ['-', 14.12,1.99,3.01,'_'],
            'sector': [12.94, '-',19.01,5.91,'/']
        })
        
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(0, result)

    def test_get_fund_performance(self) -> None:
        matrix = self._get_test_matrix({
            'fund': [5,4,3,2,1],
        })
        
        result = matrix.fund_annual_performance()
        self.assertEquals(5, len(result))
        
        self.assertEquals(5, result['Year']['value'])
        self.assertEquals('30/06/23', result['Year']['date'])
        
        self.assertEquals(4, result['Year-1']['value'])
        self.assertEquals('30/06/22', result['Year-1']['date'])

        self.assertEquals(3, result['Year-2']['value'])
        self.assertEquals('30/06/21', result['Year-2']['date'])
          
        self.assertEquals(2, result['Year-3']['value'])
        self.assertEquals('30/06/20', result['Year-3']['date'])
          
        self.assertEquals(1, result['Year-4']['value'])
        self.assertEquals('30/06/19', result['Year-4']['date'])
                  
    def test_get_fund_performance_orders_by_date(self) -> None:
    
        cols = ['30/06/22', '30/06/20','30/06/21','30/06/23', '30/06/19']
    
        matrix = self._get_test_matrix({
            'fund': [2, 4, 3, 1, 5],
        }, cols=cols)
        
        
        result = matrix.fund_annual_performance()
        self.assertEquals(5, len(result))
        
        # test the values are correct
        self.assertEquals(1, result['Year']['value'])
        self.assertEquals('30/06/23', result['Year']['date'])
        
        self.assertEquals(2, result['Year-1']['value'])
        self.assertEquals('30/06/22', result['Year-1']['date'])

        self.assertEquals(3, result['Year-2']['value'])
        self.assertEquals('30/06/21', result['Year-2']['date'])
          
        self.assertEquals(4, result['Year-3']['value'])
        self.assertEquals('30/06/20', result['Year-3']['date'])
          
        self.assertEquals(5, result['Year-4']['value'])
        self.assertEquals('30/06/19', result['Year-4']['date'])
        
    def test_fund_cumulative_performance_5_years(self) -> None:
        matrix = self._get_test_matrix({
            'fund': [10.0, 14.0, 1.0, 3.0, 1.0],
        })
        
        result = matrix.fund_cumulative_performance(5)
        self.assertEquals(31.76, result)
        
    def _get_test_matrix(self, data:dict, cols:list=[]):
        
        matrix = PerformanceMatrix()
        
        for key in ('fund','benchmark','sector','quartile'):
            
            if key in data:
                if len(cols) > 0:
                    row_data = self._test_data_provider.get_test_matrix_row_data(data[key], param_dates=cols)
                else:
                    row_data = self._test_data_provider.get_test_matrix_row_data(data[key])
                    
                row = self._container.perf_matrix_row_factory(data=row_data)
            
                matrix.add_row(key, row)
                
        return matrix