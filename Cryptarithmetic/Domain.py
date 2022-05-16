import copy


class Domain:
    

    def __init__(self, domain):

        self.domain = domain
        self.originalDomain = copy.deepcopy(domain)
        

    def addToDomain(self, value):
        if value in self.originalDomain:
            self.domain += [value]
    

    def removeFromDomain(self, value):
        if value in self.domain:
            self.domain.remove(value)
    

    def getNextFreeDomain(self):
        return self.domain[0]

        
        
    
    
        