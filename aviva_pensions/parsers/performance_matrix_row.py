"""
    a row from a performance matrix
    data is a list of dicts
    [{'date':'DD/MM/YY', 'value':percent_as_float}]
"""
class PerformanceMatrixRow:

    def __init__(self, year_cols:list[str], data:list) -> None:

        self._year_cols = year_cols

        # ensure data is sorted with the most recent date first
        self._data = sorted(data, key=lambda x: x['date'], reverse=True)

    """
        return dict of values with ending year as key
    """
    def annual_performance(self) -> dict:

        results = {}
        for i in range(0, len(self._data)):
            results[self._year_cols[i]] = self._data[i]

        return results

    def cell_at_date(self, date: str) -> float:

        for cell in self._data:
            if cell['date'] == date:
                return cell['value']
        else:
            raise KeyError('Key {} not found'.format(date))

    """
        return the average difference between this row & the other
    """
    def average_difference(self, other:'PerformanceMatrixRow') -> float:
        dates = [
            cell['date'] for cell in self._data
        ]

        total = 0.0
        for date in dates:
            total += 1.0 if self.cell_at_date(date=date) - other.cell_at_date(date=date) > 0 else 0

        return total / float(len(dates))

    """
        the cumulative return over both periods, Rc, is (1 + R1)(1 + R2) - 1 = Rc.
    """
    def cumulative_performance(self, term:int) -> float:

        if term > len(self._data):
            raise ValueError()

        total = 1
        for i in range(0, term):
            value = 1 + (self._data[i]['value']/100)
            total *= value

        return round((total - 1) * 100, 2)



