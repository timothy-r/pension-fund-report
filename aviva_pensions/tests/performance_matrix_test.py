import unittest

from aviva_pensions.parsers.performance_matrix import PerformanceMatrix

class PerformanceMatrixTest(unittest.TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_fund_to_benchmark_average_fund_higher(self):
        
        # data = {
        #     'Fund (%)': {
        #         '30/06/18 30/06/19': '12.94', 
        #         '30/06/19 30/06/20': '9.62', 
        #         '30/06/20 30/06/21': '19.01', 
        #         '30/06/21 30/06/22': '5.91', 
        #         '30/06/22 30/06/23': '8.77'
        #     }, 
        #     'Bench- mark (%)': {
        #         '30/06/18 30/06/19': '4.69', 
        #         '30/06/19 30/06/20': '4.57', 
        #         '30/06/20 30/06/21': '4.05', 
        #         '30/06/21 30/06/22': '4.36', 
        #         '30/06/22 30/06/23': '7.21'
        #     }, 
        #     'Sector Average (%)': {
        #         '30/06/18 30/06/19': '3.76',
        #         '30/06/19 30/06/20': '0.18',
        #         '30/06/20 30/06/21': '15.42',
        #         '30/06/21 30/06/22': '-6.76', 
        #         '30/06/22 30/06/23': '2.98'
        #     }, 
        #     'Quartile rank within sector': {
        #         '30/06/18 30/06/19': '3', 
        #         '30/06/19 30/06/20': '2', 
        #         '30/06/20 30/06/21': '1', 
        #         '30/06/21 30/06/22': '3', 
        #         '30/06/22 30/06/23': '4'
        #     }
        # }
        
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