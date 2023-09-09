from aviva_pensions.parsers.performance_matrix_row import PerformanceMatrixRow

"""
    A matrix of PerformanceMatrixRow instances
"""
class PerformanceMatrix:
       
    def __init__(self) -> None:
    
        self.__rows:dict[str, PerformanceMatrixRow] = {}
        
    """
        incrementally add rows to the matrix
        validate the name of the row
    """
    def add_row(self, name:str, row: PerformanceMatrixRow) -> None:
        self.__rows[name] = row
    
    """
        calculate the fund to benchmark value
        if the fund is over the benchmark in every year then the value == 1
        if it is below the benchmark in every year then the value == 0
    """
    def fund_to_benchmark_average(self) -> float:
        return self.__calculate_average('fund','benchmark')
    
    def fund_to_sector_average(self) -> float:
        return self.__calculate_average('fund','sector')

    """
        return a dict of Year, Year-1, Year-2, Year-3, Year-4 keys
        with values {'date':'DD/MM/YY', value: float}
    """
    def fund_annual_performance(self) -> dict:
        
        if 'fund' in self.__rows:
            return self.__rows['fund'].annual_performance()
        else:
            return None
    
    def fund_cumulative_performance(self, term:int) -> dict:
        if 'fund' in self.__rows:
            return self.__rows['fund'].cumulative_performance(term=term)
        else:
            return None
    
    def __calculate_average(self, from_key:str, to_key:str) -> float:
        
        if from_key in self.__rows and to_key in self.__rows:
            return self.__rows[from_key].average_difference(self.__rows[to_key])
        else:
            return None