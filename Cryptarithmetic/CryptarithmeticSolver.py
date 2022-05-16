import copy
from Constraint import SumEquals, AllDifferent
from Domain import Domain
from EncryptVar import EncryptVar


class CryptarithmeticSolver:

    def __init__(self, first, second, result):
        self.first = first
        self.second = second
        self.result = result
        self.vars = self.getVars()
        self.assignments = {'0': 0}
        self.constraints = []
        self.setConstraints()
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
            return Domain(list(range(1, 10)))
        elif len(var) == 1:
            return Domain(list(range(0, 10)))
        else:
            return Domain([0, 1])

    def setConstraints(self):
        varsCopy = copy.deepcopy(list(self.vars.keys()))
        self.constraints += [AllDifferent(varsCopy)]

        # padding the numbers with zeros.
        firstPaddingList = '0' * (len(self.result) - len(self.first))
        secondPaddingList = '0' * (len(self.result) - len(self.second))

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

        # last carry is out of result 'range'
        self.assignments[prevCarry] = 0

    def isComplete(self, result):
        if not result:
            return False
        return len(result) == (len(self.vars) + 1)

    def backtracking(self, assignments):

        if self.isComplete(assignments):
            return assignments

        # the first main point: which var to choose.
        var = self.getUnassignedVar(assignments)

        # the second main point: which value to choose.
        dom = copy.deepcopy(self.vars[var].getDomain().getDomainList())
        for value in dom:
            if self.checkConsistency(assignments, var, value):
                assignments[var] = value
                self.updateDomains(var, value)
                res = self.backtracking(assignments)
                if res != -1:
                    return res
                assignments.pop(var)
                self.cancelDomains(var, value)
        return -1

    def checkConsistency(self, ass, newVar, newValue):
        assCopy = dict(copy.deepcopy(ass))
        assCopy[newVar] = newValue
        for cons in self.constraints:
            if not cons.isConsist(assCopy):
                return False
        return True

    def getUnassignedVar(self, assignments):
        unassignedVars = list(filter(lambda x: x not in assignments, self.vars))
        return self.sortByMRV(unassignedVars)[0]

    def sortByMRV(self, unassignedVars):
        sortedDomains = sorted(unassignedVars, key=lambda x: len(self.vars[x].domain.domain))
        return sortedDomains

    def updateDomains(self, var, value):
        for v in self.vars:
            if v != var and len(var) == 1 and len(v) == 1:  # means var and v are not carry
                self.vars[v].getDomain().removeFromDomain(value)

    def cancelDomains(self, var, value):
        for v in self.vars:
            if v != var and len(var) == 1 and len(v) == 1:  # means var and v are not carry
                self.vars[v].getDomain().addToDomain(value)

