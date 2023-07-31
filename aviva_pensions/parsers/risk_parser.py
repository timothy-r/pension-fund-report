from aviva_pensions.parsers.char_stream_parser_interface import CharStreamParserInterface

"""
    Extract the risk number from a stream of pdf chars
    risks appear in a line of the chars 1 to 7
    only one risk is selected - based on the presentation
    should implement a 'char parser interface'
"""
class RiskParser(CharStreamParserInterface):
    
    def __init__(self) -> None:
        self._chars = []
        self._done = False
        
    # extract the char sequence 1-7
    def add_char(self, char:dict):
        
        if self._done:
            return
            
        if char['text'] in ['1','2','3','4','5','6','7']:
            
            if (len(self._chars) == (int(char['text']) -1)):
                self._chars.append(char)
                if len(self._chars) == 7:
                    self._done = True
            else:
                self._chars.clear()
    
    def get_chars(self):
        return self._chars

    def get_name(self):
        return 'risk'

    def get_value(self):
        if not self._done:
            return None

        for char in self._chars:
            if char['stroking_color'] == (0, 0, 0) and char['non_stroking_color'] == (0, 0, 0):
                return char['text']
        
        