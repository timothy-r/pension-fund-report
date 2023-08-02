import csv

class CSVDictReader:
    
    def __init__(self, file:str, delim:str=',', encoding:str="utf-8") -> None:
        self._file = file 
        self._delim = delim 
        self._encoding = encoding
        self._reader = None
        
    def __iter__(self):
        return self

    def __next__(self):
        # delay opening file until required
        if not self._reader:
            fh = open(file=self._file, encoding=self._encoding)
            self._reader = csv.DictReader(fh, delimiter=self._delim)
        
        return self._reader.__next__()