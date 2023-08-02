from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

class PerformancePostProcessor(PostProcessorInterface):
    
    """
        Using the performance matrix generate averages
    """
    def process(self, row: dict) -> dict:
        
        if not 'performance' in row:
            row['fund_to_benchmark_ave'] = ''
            row['fund_to_sector_ave'] = ''
            return row
        
        performance_matrix = row['performance']
        row.pop('performance')
        
        row['fund_to_benchmark_ave'] = performance_matrix.fund_to_benchmark_average()
        row['fund_to_sector_ave'] = performance_matrix.fund_to_sector_average()
        
        return row