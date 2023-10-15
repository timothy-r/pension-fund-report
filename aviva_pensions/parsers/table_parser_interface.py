import abc

class TableParserInterface:

    @abc.abstractmethod
    def read_table(self, num, table) -> None:
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_values(self) -> dict:
        pass