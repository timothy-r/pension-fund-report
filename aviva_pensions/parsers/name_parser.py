import os
import re

class NameParser:

    def parse_file_name(self, file:str) -> str:

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

    # Av Schroder Tokyo (0.98% Annual Management Charge),308
    # Av Baillie Gifford American FP (0.68% Annual Management Charge),892.1
    # remove leading Av and trailing FP
    def parse_fund_name(self, name:str) -> str:

        name = name.lstrip(' ')
        name = name.rstrip(' ')

        if name.startswith('Av '):
            items = re.search('Av (.*)', name)
            name = items.group(1)

        if name.endswith(' FP'):
            name = name.rstrip(' FP')

        return name

    def parse_label(self, label:str) -> str:

        words = label.split()

        result = []
        for word in words:
            # keep every 4th char
            chars = word[::4]
            result.append(''.join(chars))

        result = ' '.join(result)

        return result