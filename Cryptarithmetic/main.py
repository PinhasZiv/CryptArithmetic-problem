from CryptarithmeticSolver import CryptarithmeticSolver
from EncryptVar import EncryptVar


def getUserInput():    
    first = input("Enter first element: ")
    second = input("Enter second element: ")
    result = input("Enter result element: ")
    createSolver(first, second, result)
    return first, second, result

def createSolver(first, second, result):
    solver = CryptarithmeticSolver(first, second, result)
    res = solver.backtracking(solver.assignments)
    print('res: ', res)
    if res != -1:
        firstValue = int("".join(list(map(lambda c: str(res[c]), first))))
        secondValue = int("".join(list(map(lambda c: str(res[c]), second))))
        resultValue = int("".join(list(map(lambda c: str(res[c]), result))))
        
        print("first: ", firstValue)
        print("second: ", secondValue)
        print("result: ", resultValue)
        print("Succes? ", (firstValue + secondValue == resultValue))
    print("- - -")
    
getUserInput()

    
    
