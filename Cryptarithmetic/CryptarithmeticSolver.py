import copy
from Constraint import Constrait, SumEquals, AllDifferent
from Domain import Domain
from EncryptVar import EncryptVar


class CryptarithmeticSolver:
    
    def __init__(self, first, second, result):
        self.first = first
        self.second = second
        self.result = result
        self.vars = self.getVars()
        self.constraints = []
        self.setConstraints()
        self.assignments = {'0': 0}
        self.domainReduction()

    def domainReduction(self):
        fLen, sLen, rLen = len(self.first), len(self.second), len(self.result)
        
        if rLen > fLen and rLen > sLen:
            self.assignments[self.result[0]] = 1
            self.assignments['x'+str(max(len(self.first), len(self.second)) - 1)] = 1
            self.updateDomains(self.result[0], 1)
            if fLen != sLen:
                if fLen > sLen:
                    self.assignments[self.first[0]] = 9
                    self.updateDomains(self.first[0], 9)
                else:
                    self.assignments[self.second[0]] = 9
                    self.updateDomains(self.second[0], 9)

    def getVars(self):
        vars = list(set(self.first + self.second + self.result))
        varsElements = {}
        for var in vars:
            domain = self.getDomain(var)
            varsElements[var] = EncryptVar(var, domain)
        return varsElements
            
    
    def getDomain(self, var):
        firsts = [self.first[0], self.second[0], self.result[0]]
        if var in firsts:
            return Domain([0])
        elif len(var) == 1:
            return Domain()
        else:
            return Domain(list(range(2, 10)))
    
    def setConstraints(self):
        self.constraints += [AllDifferent(self.vars)]
        
        # need to to it shotrly
        firstPaddingList = ""
        for i in range(len(self.result) - len(self.first)):
            firstPaddingList += '0'
        
        secondPaddingList = ""
        for i in range(len(self.result) - len(self.second)):
            secondPaddingList += '0'
            
        
        firstRev = self.first[::-1] + firstPaddingList
        secondRev = self.second[::-1] + secondPaddingList
        resultRev = self.result[::-1]
        
        prevCarry = None
        
        for index in range(len(self.result)):
            carry = 'x' + str(index)
            domain = self.getDomain(carry)
            self.vars[carry] = EncryptVar(carry, domain)
            
            if not prevCarry:
                self.constraints += [SumEquals([firstRev[index], secondRev[index]], resultRev[index], carry)]
            else:
                self.constraints += [SumEquals([firstRev[index], secondRev[index], prevCarry], resultRev[index], carry)]
            
            prevCarry = carry
    
    
    # def connectConstraints(self):
    #     for i in range(len(self.constraints)):
    #         if i > 2:
    #             self.constraints[i].prev = self.constraints[i-1]
    #         if i >= 2 and i < len(self.constraints) - 1:
    #             self.constraints[i].next = self.constraints[i+1]
    
    def isComplete(self, result):
        if not result:
            return False
        return len(result) == len(self.vars)
    
    def backtracking(self, assinments):
        if self.isComplete(assinments):
            return self.assignments
        
        # the first main point: which var to choose.
        var = self.getUnassignedVar()
        
        # freeDomain = self.getFreeDomain(var, self.assignments)
        # the second main point: which value to choose.
        for value in self.vars[var].domain.domain:
            assinments = dict(copy.deepcopy(self.assignments))
            assinments[var] = value
            if self.checkConsistency(assinments):
                self.assignments[var] = value
                self.updateDomains(var, value)  
                res = self.backtracking(self.assignments)
                if res != -1:
                    return res
                self.assignments.pop(var)
                self.cancelDomains(var, value)
        return -1
    
    def checkConsistency(self, ass):
        for cons in self.constraints:
            if not cons.isConsist(ass):
                return False
        return True
             
    def getUnassignedVar(self):
        li = list(filter(lambda x: x not in self.assignments, self.vars))
        return li[0]
        
        # return self.sortByMRV(unssignedVars)
            
    def sortByMRV(self, unssignedVars):
        sortedDomains = sorted(unssignedVars, key=lambda x: sum(self.domains[x].domain))
        return sortedDomains
             
    
    # def getFreeDomain(self, var, assignment):
    #     index = 0
    #     freeDomains = []
    #     for domain in self.domains[var].domain:
    #         if var in assignment:
    #             if index == assignment[var]:
    #                 continue
    #         if domain:
    #             freeDomains += [index]
    #         index += 1
    #     return freeDomains


    def updateDomains(self, var, value):
        for v in self.vars:
            if v != var and len(var) == 1 and len(v) == 1: # means var and v are not carry
                self.vars[v].domain.removeFromDomain(value)
    
    def cancelDomains(self, var, value):
        for v in self.vars:
            if v != var and len(var) == 1 and len(v) == 1: # means var and v are not carry
                self.vars[v].domain.addToDomain(value)
                