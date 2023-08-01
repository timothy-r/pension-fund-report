import abc

"""
    post processor takes a dict and returns the processed version of it
"""
class PostProcessorInterface():
    
    @abc.abstractmethod
    def process(self, data:dict) -> dict:
        pass