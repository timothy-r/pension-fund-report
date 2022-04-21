import sys
import os
import csv
import re 

from pathlib import Path
from unittest import result
import pdfplumber
from Plumber import Plumber

def extract_pdf_data(file:str, available):
    
    name = os.path.basename(file)
    if name.startswith('Aviva_Pension_h-FL_'):
        items = re.search('Aviva_Pension_h-FL_(.*)', name)
        # name = name.lstrip('Aviva_Pension_h-FL_')
        name = items.group(1)
    if name.endswith('.pdf'):
        name = name.rstrip('.pdf')
    if name.endswith('_FP'):
        name = name.rstrip('_FP')
    
    # find the related item in available dict
    clean_name = name.replace('_', ' ').lower()
    clean_name = clean_name.replace('-', ' ')
    if clean_name in available:
        available_data = available[clean_name]
    else:
        print("Didn't find {}".format(clean_name))
        available_data = {'charge': '', 'unit_prices': ''}
        
    with pdfplumber.open(file) as pdf:
        
        plumber = Plumber(name, pdf)
          
        return {'name': plumber.name, 
                'sedol': plumber.sedol, 
                'isin': plumber.isin, 
                'charge': available_data['charge'],
                'unit_prices': available_data['unit_prices']
            }

def read_available(file):
    results = {}
    with open(file) as f:
        reader = csv.DictReader(f)

        for item in reader:
            name = item['name'].replace('-', ' ').replace(':', ' ').lower()
            results[name] = item
            
    return results

# iterate through a directory of files
dir = sys.argv[1]
available = read_available(sys.argv[2])
outfile = sys.argv[3]

with open(outfile, 'w', newline='') as csv_outfile:
    fieldnames = ['name', 'sedol', 'isin', 'charge', 'unit_prices']
    writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    p = Path(dir)
    for file in p.iterdir():

        # print(file)
        try:
            data = extract_pdf_data(file, available)
            # print(data)
            writer.writerow(data)
        except:
            print('Error')