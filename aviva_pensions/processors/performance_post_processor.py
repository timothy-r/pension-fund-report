from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

from aviva_pensions.parsers.performance_matrix import PerformanceMatrix

class PerformancePostProcessor(PostProcessorInterface):

    def __init__(self, columns:list[str]) -> None:
        self._year_keys = columns

    """
        Using the performance matrix generate averages
    """
    def process(self, row: dict) -> dict:

        """ ensure these keys are set with defalu values """
        row['fund_to_benchmark_ave'] = ''
        row['fund_to_sector_ave'] = ''
        for key in self._year_keys:
            row[key] = ''
        row['cumulative_perf_5'] = ''
        row['cumulative_perf_3'] = ''

        if not 'performance' in row:
            return row

        performance_matrix:PerformanceMatrix = row['performance']
        row.pop('performance')

        try:
            row['fund_to_benchmark_ave'] = performance_matrix.fund_to_benchmark_average()
        except:
            pass

        try:
            row['fund_to_sector_ave'] = performance_matrix.fund_to_sector_average()
        except:
            pass

        # split performance into max 5 attributes
        # Year, Year-1 Year-2 Year-3 Year-4
        # this dict should be sorted
        try:
            annual_performance = performance_matrix.fund_annual_performance()
            for key in annual_performance.keys():
                row[key] = annual_performance[key]['value']
        except:
            pass

        try:
            row['cumulative_perf_5'] = performance_matrix.fund_cumulative_performance(5)
        except ValueError:
            pass

        try:
            row['cumulative_perf_3'] = performance_matrix.fund_cumulative_performance(3)
        except ValueError:
            pass

        return row