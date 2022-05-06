from abc import ABC, abstractmethod
# abstract class
class Constrait(ABC):

    @abstractmethod
    def isConsist(self, assignment):
        pass

class SumEquals(Constrait):
    
    def __init__(self, add1, add2, res):
        self.add1 = add1
        self.add2 = add2
        self.res = res
        self.carry0 = 0
        self.carry1 = 0
        self.prev = None
        self.next = None
        
    def isConsist(self, assignment):
        add1Val, add2Val, resVal = 0, 0, 0
        
        # first index has no carry to take.
        if not self.prev:
            varList = [self.add1, self.add2, self.res]
        elif self.next:
            if self.add1 and self.add2:
                varList = [self.add1, self.add2, self.res, self.prev.add1, self.prev.add2]
            elif self.add1:
                varList = [self.add1, self.res, self.prev.add1, self.prev.add2]
            elif self.add2:
                varList = [self.add2, self.res, self.prev.add1, self.prev.add2]
        else:
            varList = [self.res, self.prev.add1, self.prev.add2]

        for var in varList:
            if not var in assignment:
                return True
        
        if self.add1 in assignment:
            add1Val = assignment[self.add1]
        else:
            add1Val = 0
            
        if self.add2 in assignment:
            add2Val = assignment[self.add2]
        else:
            add2Val = 0
            
        resVal = assignment[self.res]
        
        if self.next:
            if add1Val + add2Val + self.carry0 >= 10:
                self.carry1 = 1
                self.next.carry0 = 1
            else:
                self.carry1 = 0
                self.next.carry0 = 0
            
        if self.prev:
            if assignment[self.prev.add1] + assignment[self.prev.add2] >= 10:
                self.carry0 = 1
            else:
                if add1Val + add2Val + self.carry0 >= 10:
                    self.carry1 = 1
                else:
                    self.carry1 = 0
                
                
        
        sum1 = add1Val + add2Val + self.carry0
        sum2 = resVal + self.carry1 * 10
        
        return sum1 == sum2
        

class AllDifferent(Constrait):
    
    def __init__(self, first, second, result):
        self.first = first
        self.second = second
        self.result = result
    
    def isConsist(self, assignment):
        # firstF, firstS, firstR = self.first[0], self.second[0], self.result[0]
        # if firstF in assignment:
        #     if assignment[firstF] == 0:
        #         return False
        # if firstS in assignment:
        #     if assignment[firstS] == 0:
        #         return False
        # if firstR in assignment:
        #     if assignment[firstR] == 0:
        #         return False
        
        
        assignemntSet = set(assignment.values())
        return len(assignemntSet) == len(assignment)