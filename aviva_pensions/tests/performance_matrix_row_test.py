import unittest

from aviva_pensions.parsers.performance_matrix_row import PerformanceMatrixRow

class PerformanceMatrixRowTest(unittest.TestCase):
    
    def test_get_cumulative_performance_for_5_years(self)->None:
        
        values = [16.90, -42.59, 45.86, 43.51, 2.27]
        
        test_data = self._get_test_data(values=values)
        
        row = PerformanceMatrixRow(data=test_data)
        
        result = row.get_cumulative_performance(5)
        
        self.assertEquals(43.67, result)
        
    def test_get_cumulative_performance_for_3_years(self)->None:
        
        values = [16.90, -42.59, 45.86, 43.51, 2.27]
        
        test_data = self._get_test_data(values=values)
        
        row = PerformanceMatrixRow(data=test_data)
        
        result = row.get_cumulative_performance(3)
        
        self.assertEquals(-2.11, result)
        
    def test_get_cumulative_performance_for_1_year(self)->None:
        
        values = [16.90, -42.59, 45.86, 43.51, 2.27]
        
        test_data = self._get_test_data(values=values)
        
        row = PerformanceMatrixRow(data=test_data)
        
        result = row.get_cumulative_performance(1)
        
        self.assertEquals(16.9, result)
             
    
    def _get_test_data(self, values:list) -> dict:
        
        result = []
        
        dates = ['30/06/23', '30/06/22', '30/06/21', '30/06/20', '30/06/19']
        
        for i in range(0, len(values)):
            result.append(
                {
                    'date': dates[i],
                    'value': values[i]
                }
            )

        return result