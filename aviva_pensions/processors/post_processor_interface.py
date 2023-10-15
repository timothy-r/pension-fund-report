import abc

class PostProcessorInterface():
    """ Interface for PostProcessor implementations
    """

    @abc.abstractmethod
    def process(self, row:dict) -> dict:
        """ Method to perform the post processing
            takes a dict and returns the processed version of it
        """
        pass
