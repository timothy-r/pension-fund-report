from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

class PerformancePostProcessor(PostProcessorInterface):
    
    def __init__(self) -> None:
        self._year_keys = ['Year', 'Year-1', 'Year-2', 'Year-3', 'Year-4']
        
    """
        Using the performance matrix generate averages
    """
    def process(self, row: dict) -> dict:
        
        if not 'performance' in row:
            row['fund_to_benchmark_ave'] = ''
            row['fund_to_sector_ave'] = ''
            for key in self._year_keys:
                row[key] = ''
            return row
        
        performance_matrix = row['performance']
        row.pop('performance')
        
        row['fund_to_benchmark_ave'] = performance_matrix.fund_to_benchmark_average()
        row['fund_to_sector_ave'] = performance_matrix.fund_to_sector_average()
        # split performance into max 5 attributes
        # Year, Year-1 Year-2 Year-3 Year-4
        # this dict should be sorted
        annual_performance = performance_matrix.get_fund_annual_performance()
        for key in annual_performance.keys():
            row[key] = annual_performance[key]['value']
        
        return row