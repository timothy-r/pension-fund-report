from aviva_pensions.processors.post_processor_interface import PostProcessorInterface

class PerformancePostProcessor(PostProcessorInterface):
    
    def process(self, data: dict) -> dict:
        return data
    