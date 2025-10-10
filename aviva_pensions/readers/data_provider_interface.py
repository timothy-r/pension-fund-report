import abc

class DataProviderInterface:

    @abc.abstractmethod
    def read_data(self) -> dict:
        pass