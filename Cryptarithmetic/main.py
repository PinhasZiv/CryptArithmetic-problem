from CryptarithmeticSolver import CryptarithmeticSolver
from EncryptVar import EncryptVar


def getUserInput():    
    first = input("Enter first element:")
    second = input("Enter second element:")
    result = input("Enter result element:")
    createSolver(first, second, result)
    return first, second, result

def createSolver(first, second, result):
    solver = CryptarithmeticSolver(first, second, result)
    x = solver.backtracking({})
    print(x)
    print("gf")
    
getUserInput()

    
    
