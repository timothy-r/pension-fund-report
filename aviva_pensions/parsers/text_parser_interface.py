import abc

class TextParserInterface:
    
    @abc.abstractmethod
    def get_name(self):
        pass
    
    @abc.abstractmethod
    def get_value(self, text:str):
        pass