class PerformanceMatrix:
    
    def __init__(self, data:dict) -> None:
        self._data = data
        
        # keys should be mapped by the parser
        self._keys = {
            'fund' : 'Fund (%)',
            'benchmark' : 'Bench- mark (%)',
            'sector_ave' : 'Sector Average (%)',
            'quart_rank_in_sector' : 'Quartile rank within sector'
        }
    
    """
        calculate the fund to benchmark value
        if the fund is over the benchmark in every year then the value == 1
        if it is below the benchmark in every year then the value == 0
    """
    def fund_to_benchmark_average(self) -> float:
        return self._calculate_average('fund','benchmark')
    
    def fund_to_sector_average(self) -> float:
        return self._calculate_average('fund','sector_ave')

    def _calculate_average(self, from_key:str, to_key:str) -> float:
        
        if self._keys[from_key] in self._data and self._keys[to_key] in self._data:
            
            from_row = self._data[self._keys[from_key]]
            to_row = self._data[self._keys[to_key]]
            
            total = 0.0
            for k in from_row.keys():
                total += 1.0 if float(from_row[k]) - float(to_row[k]) > 0 else 0
            
            return total / float(len(from_row))
        else:
            return None