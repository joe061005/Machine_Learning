import sys, parse, grader
from p6 import *

def better_board(queenList):
    #Your p7 code here
    N = len(queenList)
    solution = ""
    smallestNum = 9999999
    position = (0,0)

    attackList = getAttackList(queenList)
    for i, row in enumerate(attackList):
        for j, col in enumerate(row):
            if col < smallestNum:
                smallestNum = col
                position = (i, j)

    queenList[position[1]] = position[0]

    for x in range(N):
        tempList = []
        for y in range(N):
            if queenList[y] == x:
                tempList.append('q')
            else:
                tempList.append('.')
        solution += " ".join(tempList) + "\n"


    # remove the '\n' at the end
    return solution[:len(solution)-1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)