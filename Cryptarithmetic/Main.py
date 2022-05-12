from CryptarithmeticSolver import CryptarithmeticSolver
from EncryptVar import EncryptVar


def solver(first, second, result):
    solver = CryptarithmeticSolver(first, second, result)
    return solver.backtracking(solver.assignments)



def getUserInput():    
    first = input("Enter first element: ")
    second = input("Enter second element: ")
    result = input("Enter result element: ")
    return first, second, result

def getLegalMassege(first, second, result):
    # check if the input contains numbers
    if any(char.isdigit() for char in first+second+result):
        return "Please enter only letters (not numbers)"
    # check if the add numbers longer than the result number
    elif len(first) > len(result) or len(second) > len(result):
        return "The numbers used for adding\nmust be shorter or equal in length to the sum."
    return "legal"

def getStringAnswer(res, first, second, result):
    if res != -1:
        firstValue = int("".join(list(map(lambda c: str(res[c]), first))))
        secondValue = int("".join(list(map(lambda c: str(res[c]), second))))
        resultValue = int("".join(list(map(lambda c: str(res[c]), result))))
        strResult = str(firstValue) + " + " + str(secondValue) + " = " + str(resultValue)
        return strResult


