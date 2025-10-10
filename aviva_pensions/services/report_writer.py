import csv

class ReportWriter:

    def __init__(self, columns:list[str], outfile:str) -> None:
        self._fieldnames = columns
        self._outfile = outfile
        self._written_headers = False

    def write_data(self, data:dict) -> None:

        writer = self._open_file()

        output = {
            key:value for (key,value) in data.items() if key in self._fieldnames
        }

        writer.writerow(output)


    def _open_file(self) -> csv.DictWriter:
        if not self._written_headers:
            # truncate existing output files
            mode = 'w'
        else:
            mode = 'a'

        csv_outfile = open(self._outfile, mode=mode, newline='')
        writer = csv.DictWriter(csv_outfile, fieldnames=self._fieldnames)

        if not self._written_headers:
            self._written_headers = True
            writer.writeheader()

        return writer