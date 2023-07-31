import abc

class TableParserInterface:
    
    @abc.abstractmethod
    def read_table(self, table):
        pass
    
    @abc.abstractmethod
    def get_name(self):
        pass
    
    @abc.abstractmethod
    def get_values(self):
        pass