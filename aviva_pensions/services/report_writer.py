import csv

class ReportWriter:
    
    def __init__(self) -> None:
         # // configure output
        self._fieldnames = ['Name', 'ISIN Code', 'risk', 'fund_to_benchmark_ave', 'fund_to_sector_ave', 'Charge', 'FT ratings', "MS ratings", 'Fund Size', 'Launch date', 'Sector Ga', 'Equities', 'External fund holdings', 'SEDOL', 'Fund Manager', 'FileName',  'General', 'Foreign Exchange Risk', 'Emerging Markets', 'Smaller Companies', 'Fixed Interest', 'Derivatives', 'Cash/Money Market Funds', 'Property Funds', 'High Yield Bonds', 'Reinsured Funds']
    
    
    def write_data(self, outfile:str, data:list) -> None:
        
        with open(outfile, 'w', newline='') as csv_outfile:
            
            writer = csv.DictWriter(csv_outfile, fieldnames=self._fieldnames)
            writer.writeheader()

            for row in data:
                output = {
                    key:value for (key,value) in row.items() if key in self._fieldnames
                }
                writer.writerow(output)
        