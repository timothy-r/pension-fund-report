import sys 
import csv
import re

from numpy import array 

""" take a csv of all available funds & extract name & annual charges"""

def process_name_charge(item:str)->dict:
    # Av Artemis Income (0.78% Annual Management Charge)
    # Av BlackRock (30:70) Currency Hedged Global Equity (Aq C) (0.23% Annual Management Charge)
    
    # use the last parenthised item as the annual charge
    # remove Av prefix
    all_items = re.search('(.*)(\(.* Annual Management Charge\))', item)
    charge = all_items.group(2)
    
    charge_value = re.search('\((.*%).*', charge).group(1)
    name = all_items.group(1)
    if name.startswith('Av '):
        name_items = re.search('Av (.*)', name)
        name = name_items.group(1)
        
    name = name.rstrip(' ')
    
    if name.endswith(' FP'):
        name_items = name.split(' ')
        name_items = name_items[:-1]
        name = ' '.join(name_items)
        
    name = name.rstrip(' ')
    
    return {'name':name, 'charge': charge_value}

file = sys.argv[1]
outfile = sys.argv[2]

# open the output csv file
with open(outfile, 'w', newline='') as csv_outfile:
    fieldnames = ['name', 'charge', 'unit_prices']
    writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    with open(file) as f:
        reader = csv.DictReader(f)

        for item in reader:
            # expect Fund name,Unit prices
            name_charge = process_name_charge(item['Fund name'])
            name_charge['unit_prices'] = item['Unit prices']
            writer.writerow(name_charge)
            