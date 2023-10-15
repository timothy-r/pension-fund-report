from collections.abc import Iterable
import unittest
from unittest.suite import _TestType

class AvivaPensionsTestSuite(unittest.TestSuite):

    def __init__(self, tests: Iterable[_TestType] = ...) -> None:
        super().__init__(tests)

