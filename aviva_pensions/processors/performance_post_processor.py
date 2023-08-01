from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

class PerformancePostProcessor(PostProcessorInterface):
    
    """
        Using the performance matrix generate averages
    """
    def process(self, data: dict) -> dict:
        
        if not 'performance' in data:
            data['fund_to_benchmark_ave'] = ''
            data['fund_to_sector_ave'] = ''
            return data
        
        performance_matrix = data['performance']
        data.pop('performance')
        
        data['fund_to_benchmark_ave'] = performance_matrix.fund_to_benchmark_average()
        data['fund_to_sector_ave'] = performance_matrix.fund_to_sector_average()
        
        return data