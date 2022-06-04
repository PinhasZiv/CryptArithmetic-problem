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
        self.constraints = self.getConstraints()

        self.domainReduction()

    # Reducing the domain before the start of the run - with the help of mathematical rules
    def domainReduction(self):
        fLen, sLen, rLen = len(self.first), len(self.second), len(self.result)

        # If the length of the result is greater than the first and second numbers ->
        # the MSB of the result must be 1
        if rLen > fLen and rLen > sLen:
            self.assignments[self.result[0]] = 1
            self.assignments['x'+str(max(len(self.first), len(self.second)) - 1)] = 1
            self.updateDomains(self.result[0], 1)
            if fLen != sLen:
                # If the length of the first number is greater than the second number ->
                # the MSB of the first number must be 9 (to reach the length of the result)
                if fLen > sLen:
                    self.assignments[self.first[0]] = 9
                    self.updateDomains(self.first[0], 9)
                else:
                    self.assignments[self.second[0]] = 9
                    self.updateDomains(self.second[0], 9)

    # Return a dictionary of variables {variable: EncryptedVar}
    def getVars(self):
        vars = list(set(self.first + self.second + self.result))
        varsElements = {}
        for var in vars:
            domain = self.getDomain(var)
            varsElements[var] = EncryptVar(var, domain)
        return varsElements

    # Return an array of possible domain values for the variable given to the function
    def getDomain(self, var):
        firsts = [self.first[0], self.second[0], self.result[0]]
        # A number cannot start with the digit '0'
        if var in firsts:
            return Domain(list(range(1, 10)))
        # The carry digit can only be 0 or 1
        elif len(var) == 2:
            return Domain([0, 1])
        else:
            return Domain(list(range(0, 10)))

    # Return an array of constraints
    def getConstraints(self):
        constraints = []
        varsCopy = copy.deepcopy(list(self.vars.keys()))
        # Add a constraint of type AllDifferent
        constraints += [AllDifferent(varsCopy)]

        # padding the numbers with zeros.
        firstPaddingList = '0' * (len(self.result) - len(self.first))
        secondPaddingList = '0' * (len(self.result) - len(self.second))

        # Arrange the words in reverse to begin with the LSB digit
        firstRev = self.first[::-1] + firstPaddingList
        secondRev = self.second[::-1] + secondPaddingList
        resultRev = self.result[::-1]

        prevCarry = None

        # Initialize variables for carry numbers
        for index in range(len(self.result)):
            carry = 'x' + str(index)
            domain = self.getDomain(carry)
            self.vars[carry] = EncryptVar(carry, domain)

            # Add a constraint of type SumEquals
            if not prevCarry:
                constraints += [SumEquals([firstRev[index], secondRev[index]], resultRev[index], carry)]
            else:
                constraints += [SumEquals([firstRev[index], secondRev[index], prevCarry], resultRev[index], carry)]

            prevCarry = carry

        # last carry is out of result 'range'
        self.assignments[prevCarry] = 0
        return constraints

    # Checks if all assignments have been completed
    def isComplete(self, result):
        if not result:
            return False
        return len(result) == (len(self.vars) + 1)

    # Backtracking algorithm for finding the right assignment for the words entered
    def backtracking(self, assignments):
        if self.isComplete(assignments):
            return assignments

        # the main point: which var to choose?
        var = self.getUnassignedVar(assignments)

        # Check the possible assignments of the current character
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

    # Check whether the new assignment satisfies all the constraints
    def checkConsistency(self, ass, newVar, newValue):
        assCopy = dict(copy.deepcopy(ass))
        assCopy[newVar] = newValue
        for cons in self.constraints:
            if not cons.isConsist(assCopy):
                return False
        return True

    # Return a character that has not yet been assigned
    def getUnassignedVar(self, assignments):
        unassignedVars = list(filter(lambda x: x not in assignments, self.vars))
        return self.sortByMRV(unassignedVars)[0]

    # Sort the array of characters received according to the heuristic 'minimum remaining values'
    def sortByMRV(self, unassignedVars):
        sortedDomains = sorted(unassignedVars, key=lambda x: len(self.vars[x].domain.domain))
        return sortedDomains

    # Domains reduction for new assignment
    def updateDomains(self, var, value):
        for v in self.vars:
            if v != var and len(var) == 1 and len(v) == 1:  # means var and v are not carry
                self.vars[v].getDomain().removeFromDomain(value)

    # Cancel domains reduction after canceling an inappropriate assignment
    def cancelDomains(self, var, value):
        for v in self.vars:
            if v != var and len(var) == 1 and len(v) == 1:  # means var and v are not carry
                self.vars[v].getDomain().addToDomain(value)

