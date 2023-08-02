import csv

class ReportWriter:
    
    def __init__(self, columns:list[str]) -> None:
        self._fieldnames = columns 
    
    def write_data(self, outfile:str, data:list) -> None:
        
        with open(outfile, 'w', newline='') as csv_outfile:
            
            writer = csv.DictWriter(csv_outfile, fieldnames=self._fieldnames)
            writer.writeheader()

            for row in data:
                output = {
                    key:value for (key,value) in row.items() if key in self._fieldnames
                }
                writer.writerow(output)
        