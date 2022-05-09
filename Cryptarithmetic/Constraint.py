from abc import ABC, abstractmethod
# abstract class
class Constrait(ABC):

    @abstractmethod
    def isConsist(self, assignment):
        pass
            

class SumEquals(Constrait):
    
    def __init__(self, vars, res, carry = 0):
        self.vars = vars
        self.res = res
        self.carry = carry
        
    def isConsist(self, assignment):
        resWithCarry = 0
        varList = self.vars + [self.res, self.carry]

        for var in varList:
            if not var in assignment:
                return True
        
        if 'a' in assignment and 'b' in assignment and 'x1' in assignment:
            if assignment['b'] != 1 and assignment['a'] != 2:
                a = "aa" 
        values = list(map(lambda x: assignment[x], self.vars))                
        sumVars = sum(values)
            
        resWithCarry = assignment[self.res] + assignment[self.carry] * 10

        return sumVars == resWithCarry
        

class AllDifferent(Constrait):
    
    def __init__(self, vars):
        self.vars = vars
    
    def isConsist(self, assignment):
        filteredVars = list(filter(lambda x: x in assignment, self.vars))
        filterCarry = list(filter(lambda x: len(x) == 1, filteredVars))
        values = list(map(lambda x: assignment[x], filterCarry)) 
        valuesSet = set(values)
        return len(valuesSet) == len(values)