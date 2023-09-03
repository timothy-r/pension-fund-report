from pathlib import Path
import pdfplumber
from typing import Callable, List

from aviva_pensions.services.pdf_reader import PDFReader

"""
    iterates recursively through a directory
    reads all pdfs found
"""
class PDFExtractorService:
    
    def __init__(self, plumber_factory:Callable[..., PDFReader]) -> None:
        self.__plumber_factory = plumber_factory
        
    def read_directory(self, dir: str) -> None:
        
        for file in self.__get_dir_pdfs(dir=dir):
            yield self.__read_pdf(file)
            
    def __get_dir_pdfs(self, dir) -> list:
        
        result = []
        
        p = Path(dir)
        for file in p.iterdir():
            if file.is_file() and file.match('*.pdf'):
                result.append(file)
            elif file.is_dir():
                result += self.__get_dir_pdfs(file)
    
        return result
    
    def __read_pdf(self, file) -> dict:
        
        try:
            print("Reading {}".format(file))
            
            with pdfplumber.open(file) as pdf:
                # create a new instance of the plumber each time
                plumber = self.__plumber_factory()
                plumber.read(file_name=file, pdf=pdf)
                
                return plumber.get_data()
        except:
            print("Cannot read pdf: {}".format(file))