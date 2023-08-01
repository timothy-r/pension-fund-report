import os
import re

class FileNameParser:
    
    def parse_name(self, file:str) -> str:
    
        name = os.path.basename(file)
        
        if name.startswith('Aviva_Pension_h-FL_'):
            items = re.search('Aviva_Pension_h-FL_(.*)', name)
            name = items.group(1)
        
        if name.endswith('.pdf'):
            name = name.rstrip('.pdf')
        
        if name.endswith('_FP'):
            name = name.rstrip('_FP')
        
        # find the related item in available dict
        name = name.replace('_', ' ')
        name = name.replace('-', ' ')

        return name