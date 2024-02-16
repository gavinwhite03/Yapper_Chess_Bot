
class Move:
    
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
    def __str__(self):
            return f"Moved from {self.initial} to {self.final}"