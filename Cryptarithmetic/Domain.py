import copy


# Class for the domain of each variable
class Domain:

    def __init__(self, domain):
        self.domain = domain
        self.originalDomain = copy.deepcopy(domain)

    # add value to domain after removing assignment
    def addToDomain(self, value):
        if value in self.originalDomain:
            self.domain += [value]

    # remove value from domain after adding assignment
    def removeFromDomain(self, value):
        if value in self.domain:
            self.domain.remove(value)

    def getNextFreeDomain(self):
        return self.domain[0]

    def getDomainList(self):
        return self.domain
