import copy

class Domain:
    
    def __init__(self, forbidden = []):
        self.domain = list(filter(lambda x: x not in forbidden, list(range(10))))
        self.forbidden = forbidden
        
    def addToDomain(self, value):
        if value not in self.forbidden:
            self.domain += [value]
    
    def removeFromDomain(self, value):
        if value in self.domain:
            self.domain.remove(value)
    
    def getNextFreeDomain(self):
        return self.domain[0]

        
        
    
    
        