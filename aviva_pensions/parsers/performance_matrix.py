from aviva_pensions.parsers.performance_matrix_row import PerformanceMatrixRow

"""
    A matrix of PerformanceMatrixRow instances
"""
class PerformanceMatrix:

    def __init__(self) -> None:

        self._rows:dict[str, PerformanceMatrixRow] = {}

        # keys should be mapped by the parser
        self._data_keys = {
            'fund' : 'Fund (%)',
            'benchmark' : 'Bench- mark (%)',
            'sector_ave' : 'Sector Average (%)',
            'quart_rank_in_sector' : 'Quartile rank within sector'
        }

    """
        incrementally add rows to the matrix
        validate the name of the row
    """
    def add_row(self, name:str, row: PerformanceMatrixRow) -> None:
        self._rows[name] = row

    """
        calculate the fund to benchmark value
        if the fund is over the benchmark in every year then the value == 1
        if it is below the benchmark in every year then the value == 0
    """
    def fund_to_benchmark_average(self) -> float:
        return self._calculate_average('fund','benchmark')

    def fund_to_sector_average(self) -> float:
        return self._calculate_average('fund','sector')

    """
        return a dict of Year, Year-1, Year-2, Year-3, Year-4 keys
        with values {'date':'DD/MM/YY', value: float}
    """
    def fund_annual_performance(self) -> dict:

        if 'fund' in self._rows:
            return self._rows['fund'].annual_performance()

    def fund_cumulative_performance(self, term:int) -> dict:
        if 'fund' in self._rows:
            return self._rows['fund'].cumulative_performance(term=term)

    def _calculate_average(self, from_key:str, to_key:str) -> float:

        if from_key in self._rows and to_key in self._rows:
            return self._rows[from_key].average_difference(self._rows[to_key])
