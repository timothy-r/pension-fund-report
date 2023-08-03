"""
    a row from a performance matrix
    data is a list of dicts
    [{'date':'DD/MM/YY', 'value':percent_as_float}]
"""
class PerformanceMatrixRow:
    
    def __init__(self, data:list) -> None:
        # ensure data is sorted with the most recent date first
        self._data = sorted(data, key=lambda x: x['date'], reverse=True)
        
    # def get_annual_performance -> return dict of values with ending year as key
    
    """
        the cumulative return over both periods, Rc, is (1 + R1)(1 + R2) - 1 = Rc.
    """
    def get_cumulative_performance(self, term:int) -> float:
        
        if term > len(self._data):
            raise ValueError()
        
        total = 1
        for i in range(0, term):
            value = 1 + (self._data[i]['value']/100)
            total *= value
        
        return round((total - 1) * 100, 2)
        
        
    
    