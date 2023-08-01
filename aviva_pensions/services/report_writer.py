import csv

class ReportWriter:
    
    def __init__(self) -> None:
         # // configure output
        self._fieldnames = ['Name', 'Fund Size', 'Launch date', 'Sector Ga', 'Equities', 'External fund holdings', 'SEDOL', 'Fund Manager', 'ISIN Code', 'risk', 'General', 'Foreign Exchange Risk', 'Emerging Markets', 'Smaller Companies', 'Fixed Interest', 'Derivatives', 'Cash/Money Market Funds', 'Property Funds', 'High Yield Bonds', 'Reinsured Funds']
    
    
    def write_data(self, outfile:str, data:list) -> None:
        
        with open(outfile, 'w', newline='') as csv_outfile:
            
            writer = csv.DictWriter(csv_outfile, fieldnames=self._fieldnames)
            writer.writeheader()

            for row in data:
                output = {
                    key:value for (key,value) in row.items() if key in self._fieldnames
                }
                writer.writerow(output)
        