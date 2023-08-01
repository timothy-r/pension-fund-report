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
        fund_row = self._data[self._keys['fund']]
        bench_mark_row = self._data[self._keys['benchmark']]
        total = 0.0
        for k in fund_row.keys():
            total += 1.0 if float(fund_row[k]) - float(bench_mark_row[k]) > 0 else 0
        
        return total / float(len(fund_row))
    
            