import abc

class TextParserInterface:

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_values(self, text:str) -> dict:
        pass