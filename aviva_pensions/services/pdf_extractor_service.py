from pathlib import Path
import pdfplumber
from typing import Callable, List

from aviva_pensions.services.plumber import Plumber

"""
    iterates recursively through a directory
    reads all pdfs found
"""
class PDFExtractorService:

    def __init__(self, plumber_factory:Callable[..., Plumber]) -> None:
        self._plumber_factory = plumber_factory

    def read_directory(self, dir: str) -> None:

        for file in self._get_dir_pdfs(dir=dir):
            yield self._read_pdf(file)

    def _get_dir_pdfs(self, dir) -> list:

        result = []

        p = Path(dir)
        for file in p.iterdir():
            if file.is_file() and file.match('*.pdf'):
                result.append(file)
            elif file.is_dir():
                result += self._get_dir_pdfs(file)

        return result

    def _read_pdf(self, file) -> dict:

        try:
            print("Reading {}".format(file))

            with pdfplumber.open(file) as pdf:
                # create a new instance of the plumber each time
                plumber = self._plumber_factory()
                plumber.read(file_name=file, pdf=pdf)

                return plumber.get_data()
        except:
            print("Cannot read pdf: {}".format(file))