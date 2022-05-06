
import copy


class Domain:
    
    def __init__(self):
        self.domain = [True for i in range(10)]
    
    def setDomain(self, index, value):
        self.domain[index] = value
    
    # set index=True, all the rest = False  
    def updateDomain(self, index):
        self.domain[index] = True
            # else:
            #     self.domain[i] = False
    
    # update other domain:
    # index = False, all the rest: no change        
    def updateOtherDomains(self, index):
        self.domain[index] = False
    
    def cancelDomain(self, index):
        self.domain[index] = True
    
    def cancelOtherDomains(self, index):
        self.domain[index] = True

        
        
    
    
        