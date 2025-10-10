import unittest

from aviva_pensions.parsers.performance_matrix_row import PerformanceMatrixRow
from aviva_pensions.tests.test_data_provider import TestDataProvider

class PerformanceMatrixRowTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self._year_cols = ["Year", "Year-1", "Year-2", "Year-3", "Year-4"]
        self._test_data_provider = TestDataProvider()

    def test_get_cumulative_performance_for_5_years(self)->None:

        values = [16.90, -42.59, 45.86, 43.51, 2.27]

        test_data = self._test_data_provider.get_test_matrix_row_data(values=values)

        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data)

        result = row.cumulative_performance(5)

        self.assertEqual(43.67, result)

    def test_get_cumulative_performance_for_3_years(self)->None:

        values = [16.90, -42.59, 45.86, 43.51, 2.27]

        test_data = self._test_data_provider.get_test_matrix_row_data(values=values)


        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data)

        result = row.cumulative_performance(3)

        self.assertEqual(-2.11, result)

    def test_get_cumulative_performance_for_1_year(self)->None:

        values = [16.90, -42.59, 45.86, 43.51, 2.27]

        test_data = self._test_data_provider.get_test_matrix_row_data(values=values)

        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data)

        result = row.cumulative_performance(1)

        self.assertEqual(16.9, result)


    def test_cell_at(self) -> None:
        values = [16.90, -42.59, 45.86, 43.51, 2.27]

        test_data = self._test_data_provider.get_test_matrix_row_data(values=values)

        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data)

        self.assertEqual(16.90, row.cell_at_date('30/06/23'))
        self.assertEqual(-42.59, row.cell_at_date('30/06/22'))

    def test_average_difference(self) -> None:

        values_1 = [10.0, 20.0, 40.0, 30.0, 1.0]

        test_data_1 = self._test_data_provider.get_test_matrix_row_data(values=values_1)

        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data_1)

        values_2 = [1.0, 2.0, 4.0, 3.0, 0.10]

        test_data_2 = self._test_data_provider.get_test_matrix_row_data(values=values_2)

        other_row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data_2)

        result = row.average_difference(other=other_row)

        self.assertEqual(1, result)

    def test_average_difference_2(self) -> None:

        values_1 = [10.0, 20.0, 40.0, 30.0, 1.0]

        test_data_1 = self._test_data_provider.get_test_matrix_row_data(values=values_1)

        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data_1)

        values_2 = [20.0, 30.0, 50.0, 3.0, 0.10]
        test_data_2 = self._test_data_provider.get_test_matrix_row_data(values=values_2)
        other_row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data_2)

        result = row.average_difference(other=other_row)

        self.assertEqual(0.4, result)

    def test_annual_performance(self) -> None:
        values = [16.90, -42.59, 45.86, 43.51, 2.27]

        test_data = self._test_data_provider.get_test_matrix_row_data(values=values)

        row = PerformanceMatrixRow(year_cols=self._year_cols, data=test_data)

        result = row.annual_performance()
        self.assertEqual(16.90, result['Year']['value'])
        self.assertEqual('30/06/23', result['Year']['date'])

