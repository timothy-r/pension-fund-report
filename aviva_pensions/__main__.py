import sys
import csv
from dependency_injector.wiring import Provide, inject

from aviva_pensions.container import Container

from aviva_pensions.services.pdf_reporter import PDFReporter

@inject
def main(
    dir:str, 
    outfile:str,
    pdf_reporter: PDFReporter = Provide[Container.pdf_reporter]
) -> None:
    
    # read all pdfs from directory
    # print out extracted data from each pdf
    results = pdf_reporter.read_directory(dir)
    
    # print(results)
    
    # fieldnames = results[0].keys()
    
    fieldnames = ['Name', 'Fund Size', 'Launch date', 'Sector Ga', 'Equities', 'External fund holdings', 'SEDOL', 'Fund Manager', 'ISIN Code', 'risk', 'General', 'Foreign Exchange Risk', 'Emerging Markets', 'Smaller Companies', 'Fixed Interest', 'Derivatives', 'Cash/Money Market Funds', 'Property Funds', 'High Yield Bonds', 'Reinsured Funds']
    
    with open(outfile, 'w', newline='') as csv_outfile:
        writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in results:
            output = {
                key:value for (key,value) in row.items() if key in fieldnames
            }
            writer.writerow(output)
    
    
if __name__ == "__main__":
    
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])