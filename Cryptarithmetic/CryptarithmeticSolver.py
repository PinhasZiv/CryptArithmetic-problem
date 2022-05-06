import copy
from Constraint import Constrait, SumEquals, AllDifferent
from Domain import Domain
from EncryptVar import EncryptVar


class CryptarithmeticSolver:
    
    def __init__(self, first, second, result):
        self.first = first
        self.second = second
        self.result = result
        self.vars = {}
        self.charsNum = 0
        self.setVars()
        self.domains = {}
        self.setDomains()
        self.assignments = {}
        self.constraints = []
        self.setConstraints()
        self.connectConstraints()
        self.domainReduction()

    def domainReduction(self):
        # remove 0 from domains of MSB letters (number can't starts from 0)
        if len(self.first) > 1:
            self.domains[self.first[0]].setDomain(0, False)
        if len(self.second) > 1:
            self.domains[self.second[0]].setDomain(0, False)
        if len(self.result) > 1:
            self.domains[self.result[0]].setDomain(0, False)
        
        if len(self.result) > len(self.first) and len(self.result) > len(self.second):
            self.assignments[self.result[0]] = 1
            self.updateDomains(self.result[0], 1)

    def setVars(self):
        vars = list(set(self.first + self.second + self.result))
        self.charsNum = len(vars)
        addVars = min(len(self.first), len(self.second))
        varsSize = 0
        for char in vars:
            self.vars[char] = EncryptVar(char)
        varsSize = len(self.vars)
    
    def setDomains(self):
        for var in self.vars:
            self.domains[var] = Domain()

      
    def setConstraints(self):
        firstRev, secondRev, resultRev = self.first[::-1],self.second[::-1], self.result[::-1]
        self.constraints += [AllDifferent(self.first, self.second, self.result)]
        for index in range(len(self.result)):
                
            if index < len(self.first) and index < len(self.second):
                add1, add2 = firstRev[index], secondRev[index]
                res = resultRev[index]
                self.constraints += [SumEquals(add1, add2, res)]
                continue
            
            if index < len(self.first):
                add1, add2 = firstRev[index], 0
                res = resultRev[index]
                self.constraints += [SumEquals(add1, add2, res)]
                continue
            
            if index < len(self.second):
                add1, add2 = 0, secondRev[index]
                res = resultRev[index]
                self.constraints += [SumEquals(add1, add2, res)]
                continue
            
            if index == len(self.result) - 1 and len(self.first) == len(self.second):
                add1, add2 = 0, 0
                res = resultRev[index]
                self.assignments[res] = 1
                self.updateDomains(res, 1)
                self.constraints += [SumEquals(add1, add2, res)]
            else:
                add1, add2 = 0, 0
                res = resultRev[index]
                self.constraints += [SumEquals(add1, add2, res)]
    
    
    def connectConstraints(self):
        for i in range(len(self.constraints)):
            if i > 1:
                self.constraints[i].prev = self.constraints[i-1]
            if i >= 1 and i < len(self.constraints) - 1:
                self.constraints[i].next = self.constraints[i+1]
    
    def isComplete(self, result):
        if not result:
            return False
        return len(result) == self.charsNum
    
    def backtracking(self, assinments):
        if self.isComplete(assinments):
            return self.assignments
        unssignedVars = self.getUnssignedVars()
        # the first main point: which var to choose.
        var = unssignedVars[0]
        freeDomain = self.getFreeDomain(var, self.assignments)
        # the second main point: which value to choose.
        for domain in freeDomain:
            assinments = dict(copy.deepcopy(self.assignments))
            assinments[var] = domain
            # self.assignments[var] = domain
            # self.updateDomains(var, domain)
            if self.checkVarConsistency(assinments):
                self.assignments[var] = domain
                self.updateDomains(var, domain)  
                res = self.backtracking(self.assignments)
                if res != -1:
                    return res
                self.assignments.pop(var)
                self.cancelDomains(var, domain)
        return -1
    
    def checkVarConsistency(self, ass):
        for cons in self.constraints:
            if not cons.isConsist(ass):
                return False
        return True
             
    def getUnssignedVars(self):
        vars = list(copy.deepcopy(self.vars))
        unssignedVars = []
        for var in vars:
            if not var in self.assignments:
                unssignedVars += [var]
        return unssignedVars
    
    def getFreeDomain(self, var, assignment):
        index = 0
        freeDomains = []
        for domain in self.domains[var].domain:
            if var in assignment:
                if index == assignment[var]:
                    continue
            if domain:
                freeDomains += [index]
            index += 1
        return freeDomains


    def updateDomains(self, var, index):
        for dom in self.domains:
            if dom != var:
                self.domains[dom].updateOtherDomains(index)
    
    def cancelDomains(self, var, index):
        for dom in self.domains:
            if dom != var:
                self.domains[dom].cancelOtherDomains(index)
                