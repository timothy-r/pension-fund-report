from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

from aviva_pensions.parsers.performance_matrix import PerformanceMatrix

class PerformancePostProcessor(PostProcessorInterface):

    def __init__(self, columns:list[str]) -> None:
        self._year_keys = columns

    """
        Using the performance matrix generate averages
    """
    def process(self, target_row: dict) -> dict:

        """ ensure these keys are set with defalu values """
        target_row['fund_to_benchmark_ave'] = ''
        target_row['fund_to_sector_ave'] = ''
        for key in self._year_keys:
            target_row[key] = ''
        target_row['cumulative_perf_5'] = ''
        target_row['cumulative_perf_3'] = ''

        if not 'performance' in target_row:
            return target_row

        performance_matrix:PerformanceMatrix = target_row['performance']
        target_row.pop('performance')

        try:
            target_row['fund_to_benchmark_ave'] = performance_matrix.fund_to_benchmark_average()
        except:
            pass

        try:
            target_row['fund_to_sector_ave'] = performance_matrix.fund_to_sector_average()
        except:
            pass

        # split performance into max 5 attributes
        # Year, Year-1 Year-2 Year-3 Year-4
        # this dict should be sorted
        try:
            annual_performance = performance_matrix.fund_annual_performance()
            for key in annual_performance.keys():
                target_row[key] = annual_performance[key]['value']
        except:
            pass

        try:
            target_row['cumulative_perf_5'] = performance_matrix.fund_cumulative_performance(5)
        except ValueError:
            pass

        try:
            target_row['cumulative_perf_3'] = performance_matrix.fund_cumulative_performance(3)
        except ValueError:
            pass

        return target_row