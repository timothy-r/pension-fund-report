class TestDataProvider:

    def get_test_matrix_row_data(self, values:list, param_dates:list =[]) -> dict:

        result = []
        if len(param_dates) > 0:
            dates = param_dates
        else:

            dates = ['30/06/23', '30/06/22', '30/06/21', '30/06/20', '30/06/19']

        for i in range(0, len(values)):
            result.append(
                {
                    'date': dates[i],
                    'value': values[i]
                }
            )

        return result