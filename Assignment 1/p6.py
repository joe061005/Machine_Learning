import sys, parse, grader


def number_of_attacks(queenList):
    # Your p6 code here
    solution = ""
    N = len(queenList)

    for x in range(N):
        attackNumList = []
        for y in range(N):
            tempoqueenList = queenList.copy()
            tempoqueenList[y] = x
            attackNumList.append(str(getAttackNum(tempoqueenList, N)))
        if len("".join(attackNumList)) == 16:
            solution += " ".join(attackNumList) + "\n"
        else:
            tempStr = ""
            for char in attackNumList:
                if len(str(char)) == 1:
                    tempStr += " " + str(char) + " "
                else:
                    tempStr += str(char) + " "
            solution += " " + tempStr.strip() + "\n"

    # delete '\n' at the end
    return solution[:len(solution)-1]

def getAttackList(queenList):
    N = len(queenList)
    attackNumList = []

    for x in range(N):
        tempoList = []
        for y in range(N):
            tempoqueenList = queenList.copy()
            tempoqueenList[y] = x
            tempoList.append(getAttackNum(tempoqueenList, N))
        attackNumList.append(tempoList)

    # delete '\n' at the end
    return attackNumList


def getAttackNum(queenList, N):
    attackNum = 0

    for colNo in range(N):
        rowNo = queenList[colNo]

        tempColNo = colNo
        # upper diagonal on right side
        for x in range(rowNo - 1, -1, -1):
            tempColNo += 1
            if tempColNo == N:
                break
            if queenList[tempColNo] == x:
                attackNum += 1

        tempColNo = colNo
        # lower diagonal on right side
        for x in range(rowNo + 1, N):
            tempColNo += 1
            if tempColNo == N:
                break
            if queenList[tempColNo] == x:
                attackNum += 1

        # right side
        for y in range(colNo+1, N):
            if queenList[y] == rowNo:
                attackNum += 1

    return attackNum

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)
