class TableCellLabelParser:
    
    def parse_label(self, label) -> str:
        
        words = label.split()
        
        result = []
        for word in words:
            # keep every 4th char
            chars = word[::4]
            result.append(''.join(chars))
        
        result = ' '.join(result)
        
        return result