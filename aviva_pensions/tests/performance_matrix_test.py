import unittest

from aviva_pensions.parsers.performance_matrix import PerformanceMatrix

class PerformanceMatrixTest(unittest.TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_fund_to_benchmark_average_fund_higher(self):
        
        data = self._get_test_matrix({
            'fund': ['12.94', '9.62','19.01','5.91','8.77'],
            'benchmark': ['10.05', '4.12','1.99','3.01','1.03']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(1, result)
    
    def test_fund_to_benchmark_average_fund_lower(self):
        data = self._get_test_matrix({
            'fund': ['10.05', '4.12','1.99','3.01','1.03'],
            'benchmark':['12.94', '9.62','19.01','5.91','8.77']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(0, result)
    
    def test_fund_to_benchmark_average_fund_60_percent(self):
        data = self._get_test_matrix({
            'fund': ['10.05', '4.12','17.99','9.01','1.03'],
            'benchmark':['12.94', '1.62','11.01','5.91','8.77']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(0.6, result)
    
    def test_fund_to_benchmark_average_fund_validates_data(self):
        matrix = PerformanceMatrix({})
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(None, result)
    
    def test_fund_to_benchmark_average_handles_strings(self):
        data = self._get_test_matrix({
            'fund': ['-', '14.12','1.99','3.01','_'],
            'benchmark': ['12.94', '-','19.01','5.91','/']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(0, result)
        
    def test_fund_to_sector_average_validates_data(self):
        matrix = PerformanceMatrix({})
        result = matrix.fund_to_benchmark_average()
        
        self.assertEquals(None, result)

    def test_fund_to_sector_average_fund_higher(self):
        data = self._get_test_matrix({
            'fund': ['12.94', '9.62','19.01','5.91','8.77'],
            'sector': ['10.05', '4.12','1.99','3.01','1.03']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(1, result)

    def test_fund_to_sector_average_fund_lower(self):
        data = self._get_test_matrix({
            'fund': ['10.05', '4.12','1.99','3.01','1.03'],
            'sector': ['12.94', '9.62','19.01','5.91','8.77']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(0, result)

    def test_fund_to_sector_average_fund_20_percent(self):
        data = self._get_test_matrix({
            'fund': ['10.05', '14.12','1.99','3.01','1.03'],
            'sector': ['12.94', '9.62','19.01','5.91','8.77']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(0.2, result)

    def test_fund_to_sector_average_handles_strings(self):
        data = self._get_test_matrix({
            'fund': ['-', '14.12','1.99','3.01','_'],
            'sector': ['12.94', '-','19.01','5.91','/']
        })
        
        matrix = PerformanceMatrix(data)
        result = matrix.fund_to_sector_average()
        
        self.assertEquals(0, result)

    def test_get_fund_performance(self) -> None:
        data = self._get_test_matrix({
            'fund': ['10.05', '14.12','1.99','3.01','1.03'],
        })
        
        matrix = PerformanceMatrix(data=data)
        result = matrix.get_fund_annual_performance()
        self.assertEquals(5, len(result))
        self.assertEquals('10.05', result['30/06/19'])
        self.assertEquals('14.12', result['30/06/20'])
        self.assertEquals('1.99', result['30/06/21'])
        self.assertEquals('3.01', result['30/06/22'])
        self.assertEquals('1.03', result['30/06/23'])
        
    def _get_test_matrix(self, data:dict):
        keys = {'fund':'Fund (%)','benchmark':'Bench- mark (%)','sector':'Sector Average (%)','quartile':'Quartile rank within sector'}
        
        cols = ['30/06/18 30/06/19', '30/06/19 30/06/20','30/06/20 30/06/21','30/06/21 30/06/22','30/06/22 30/06/23']
        matrix = {}
        
        for key in ('fund','benchmark','sector','quartile'):
        
            if key in data:
                matrix[keys[key]] = {}
                
                for i in range(0, len(data[key])):
                    matrix[keys[key]][cols[i]] = data[key][i]
        
        return matrix