
class EncryptVar:
    
    def __init__(self, var):
        self.var = var
        self.value = -1
        self.constraints = []
        self.consCounter = 0
    
    def getVar(self):
        return self.var
    
    def getValue(self):
        return self.value
    
    def getContraints(self):
        return self.constraints
    
    def getConsCounter(self):
        return self.consCounter
    
    def setValue(self, newVal):
        self.value = newVal
    
    def setConstraints(self, var):
        self.constraints += [var]
        
    def addConsCounter(self):
        self.consCounter += 1
        