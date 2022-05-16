from abc import ABC, abstractmethod
# abstract class
class Constrait(ABC):

    @abstractmethod
    def isConsist(self, assignment):
        pass
            

class SumEquals(Constrait):
    
    def __init__(self, vars, res, carry = '0'):
        self.vars = vars
        self.res = res
        self.carry = carry
        self.varList = self.vars + [self.res, self.carry]
        
    def isConsist(self, assignment):
        
        for var in self.varList:
            if var not in assignment:
                return True
        
        values = list(map(lambda x: assignment[x], self.vars))                
        sumVars = sum(values)
            
        resWithCarry = assignment[self.res] + (assignment[self.carry] * 10)

        return (sumVars == resWithCarry)
        

class AllDifferent(Constrait):
    
    def __init__(self, vars):
        self.vars = vars
    
    def isConsist(self, assignment):
        filteredVars = list(filter(lambda x: (x in assignment) and (len(x) == 1), self.vars))
        values = list(map(lambda x: assignment[x], filteredVars)) 
        valuesSet = set(values)
        return len(valuesSet) == len(values)