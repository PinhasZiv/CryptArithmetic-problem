from CryptarithmeticSolver import CryptarithmeticSolver


def getUserInput():
    first = input("Enter first element: ")
    second = input("Enter second element: ")
    result = input("Enter result element: ")
    return first, second, result


def getLegalMessage(first, second, result):
    # check if one of the inputs is empty
    if first == "" or second == "" or result == "":
        return "Please fill all inputs"
    # check if more than ten different characters have been entered
    if len(set(first + second + result)) > 10:
        return "You cannot enter more than ten different characters."
    # check if the input contains numbers
    if any(char.isdigit() for char in first+second+result):
        return "Please enter only letters (not numbers)"
    # check if the add numbers longer than the result number
    elif len(first) > len(result) or len(second) > len(result):
        return "The numbers used for adding\nmust be shorter or equal in length to the sum."
    return "legal"


def solveProblem(first, second, result):
    solver = CryptarithmeticSolver(first, second, result)
    return solver.backtracking(solver.assignments)


def getStringAnswer(res, first, second, result):
    if res != -1:
        firstValue = int("".join(list(map(lambda c: str(res[c]), first))))
        secondValue = int("".join(list(map(lambda c: str(res[c]), second))))
        resultValue = int("".join(list(map(lambda c: str(res[c]), result))))
        strResult = "Result: " + str(firstValue) + " + " + str(secondValue) + " = " + str(resultValue)
        return strResult


