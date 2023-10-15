import unittest

from aviva_pensions.tests.add_columns_post_processor_test import AddColumnsPostProcessorTest
from aviva_pensions.tests.name_parser_test import NameParserTest
from aviva_pensions.tests.performance_matrix_row_test import PerformanceMatrixRowTest
from aviva_pensions.tests.performance_matrix_test import PerformanceMatrixTest
from aviva_pensions.tests.performance_table_parser_test import PerformanceTableParserTest
from aviva_pensions.tests.risk_parser_test import RiskParserTest

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite()

    suite.addTest(AddColumnsPostProcessorTest())
    suite.addTest(NameParserTest())
    suite.addTest(PerformanceMatrixRowTest())
    suite.addTest(PerformanceMatrixTest())
    suite.addTest(PerformanceTableParserTest())
    suite.addTest(RiskParserTest())

    runner.run(suite)
