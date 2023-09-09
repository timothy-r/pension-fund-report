from html.parser import HTMLParser
import re

"""
    extract urls for a specified domain from a HTML string
"""
class URLParser(HTMLParser):
    
    """
        eg www.my-domain.com
    """
    def __init__(self, scheme_domain:str) -> None:
        
        self.__scheme_domain = scheme_domain
        self.__urls = []
        self.__attr = 'onclick'
    
    """
        extract urls
    """
    def parse(self, html:str):
        self.feed(html)
        for url in self.__urls:
            yield url
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            url = self.__extract_url(attrs=attrs)
            if url:
                self.__urls.append(url)
    
    def __extract_url(self, attrs):
        
        pattern = "{}'".format(self.__scheme_domain)
        
        for attr in attrs:
            if attr[0] == self.__attr:
                # extract url using http:// pattern ending with '
                match = re.search(pattern, attr[1])
                if match:
                    return match
        
        return None