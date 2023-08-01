from pathlib import Path
import pdfplumber
from typing import Callable, List

from aviva_pensions.services.plumber import Plumber

class PDFExtractorService:
    
    def __init__(self, plumber_factory:Callable[..., Plumber]) -> None:
        self._plumber_factory = plumber_factory
        
    def read_directory(self, dir: str):
        
        results = []
        
        p = Path(dir)
        for file in p.iterdir():
            
            row = self._read_pdf(file)
            if row:
                results.append(row)
                
        return results
    
    def _read_pdf(self, file):
        # only read
        
        try:
            with pdfplumber.open(file) as pdf:
                # create a new instance of the plumber each time
                plumber = self._plumber_factory()
                plumber.read(file_name=file, pdf= pdf)
                
                return plumber.get_data()
        except:
            print("Cannot read pdf: {}".format(file))