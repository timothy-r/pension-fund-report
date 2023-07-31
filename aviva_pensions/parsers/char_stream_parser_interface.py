import abc

class CharStreamParserInterface:
    
    @abc.abstractmethod
    def add_char(self, char:dict) -> None:
        pass
    
    @abc.abstractmethod
    def get_name(self) -> str:
        pass
    
    @abc.abstractmethod
    def get_values(self) -> dict:
        pass