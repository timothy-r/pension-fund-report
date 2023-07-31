import abc

class CharStreamParserInterface:
    
    @abc.abstractmethod
    def add_char(self, char:dict):
        pass
    
    @abc.abstractmethod
    def get_name(self):
        pass
    
    @abc.abstractmethod
    def get_value(self):
        pass