from abc import ABC, abstractmethod
# abstract class
class Constrait(ABC):

    @abstractmethod
    def isConsist(self, assignment):
        pass
            

class SumEquals(Constrait):
    
    def __init__(self, vars, res, carry):
        self.vars = vars
        self.res = res
        self.carry = carry
        
    def isConsist(self, assignment):
        add1Val, add2Val, resWithCarry = 0, 0, 0
        varList = self.vars + [self.res]

        for var in varList:
            if not var in assignment:
                return True
        
        values = list(map(lambda x: assignment[x], self.vars))                
        sumVars = sum(values)
        resWithCarry = assignment[self.res] + assignment[self.carry] * 10

        return sumVars == resWithCarry
        

class AllDifferent(Constrait):
    
    def __init__(self, vars):
        self.vars = vars
    
    def isConsist(self, assignment):
        filteredVars = list(filter(lambda x: x in assignment, self.vars))
        values = list(map(lambda x: assignment[x], filteredVars)) 
        valuesSet = set(values)
        return len(valuesSet) == len(values)