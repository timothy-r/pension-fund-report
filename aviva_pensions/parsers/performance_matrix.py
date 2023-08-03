
"""
    consider creating a PerformanceMatrixRow class
"""
class PerformanceMatrix:
       
    def __init__(self, columns:list[str], data:dict) -> None:
    
        self._year_keys = columns
        self._data = data
        
        # keys should be mapped by the parser
        self._data_keys = {
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

    """
        return a dict of Year, Year-1, Year-2, Year-3, Year-4 keys
        with values {'date':'DD/MM/YY', value: float}
        return a dict of DD/MM/YY => annual_performance
        sort by date
    """
    def get_fund_annual_performance(self) -> dict:
        temp_results = {}
        main_key = self._data_keys['fund']
        
        if not main_key in self._data:
            # or raise an exception??
            return {}
        
        keys = []
        
        # parser should extract correct keys
        for key in self._data[main_key].keys():
            new_key = key.split(' ')[-1]
            keys.append(new_key)
            temp_results[new_key] = self._data[main_key][key]
        
        # sort & create a new dict
        keys.sort(reverse=True)
        
        results = {}
        for i in range(0, len(keys)):
            
            results[self._year_keys[i]] = {
                'date': keys[i],
                'value': temp_results[keys[i]]
            }
            
        return results
    
    def _calculate_average(self, from_key:str, to_key:str) -> float:
        
        if self._data_keys[from_key] in self._data and self._data_keys[to_key] in self._data:
            
            from_row = self._data[self._data_keys[from_key]]
            to_row = self._data[self._data_keys[to_key]]
            
            total = 0.0
            for k in from_row.keys():
                try:
                    total += 1.0 if float(from_row[k]) - float(to_row[k]) > 0 else 0
                except ValueError:
                    pass
                
            return total / float(len(from_row))
        else:
            return None