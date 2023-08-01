from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

class PostProcessorService:
    
    """
        initialise with processors that implement an interface
    """
    def __init__(self, post_processors:list[PostProcessorInterface]) -> None:
        self._post_processors = post_processors
    
    def process(self, data:dict) -> dict:
        
        # result = data
        for p in self._post_processors:
            print(p)
            data = p.process(data=data)
        
        return data
    
    