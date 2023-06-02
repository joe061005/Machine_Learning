import sys, grader, parse, random
from decimal import Decimal


def play_episode(problem):
    if problem['seed'] != -1:
        random.seed(problem['seed'], version=1)
    d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    terminate = False
    experience = getInitialString(problem['grid'], problem['state'])
    totalReward = 0
    while not terminate:
        currentState = problem['present']
        a = problem['policy'][currentState[0]][currentState[1]]
        choice = random.choices(population=d[a], weights=[1 - problem['noise'] * 2, problem['noise'], problem['noise']])[0]
        terminate, totalLivingReward, reward, finalReward,  = updateState(problem['grid'], problem['present'], problem['livingReward'], choice, totalReward, len(problem['grid']), len(problem['grid'][0]))
        totalReward = totalLivingReward
        if len(str(totalLivingReward).split(".")[1]) > 2:
            totalLivingReward = round(totalLivingReward, 2)
        experience += getupdatedString(choice, a, reward, totalLivingReward, problem['grid'], problem['state'])
        if terminate:
            totalLivingReward += finalReward
            experience += getExitString(finalReward, totalLivingReward, problem['grid'], problem['state'], problem['present'])



    return experience


def updateState(grid, presentState, livingReward, direction, totalLivingReward, rMax, cMax):
    l = ['_', '#', 'S', 'P']
    terminate = False
    finalReward = 0
    if direction == 'N' and presentState[0] - 1 >= 0 and grid[presentState[0] - 1][presentState[1]] != "#":
        if grid[presentState[0] - 1][presentState[1]] not in l:
            terminate = True
            finalReward = float(grid[presentState[0] - 1][presentState[1]])

        totalLivingReward += float(livingReward)
        grid[presentState[0] - 1][presentState[1]] = 'P'
        grid[presentState[0]][presentState[1]] = '_'
        presentState[0] = presentState[0] - 1
    elif direction == 'E' and presentState[1] + 1 < cMax and grid[presentState[0]][presentState[1] + 1] != "#":
        if grid[presentState[0]][presentState[1]+1] not in l:
            terminate = True
            finalReward = float(grid[presentState[0]][presentState[1]+1])

        totalLivingReward += float(livingReward)
        grid[presentState[0]][presentState[1] + 1] = 'P'
        grid[presentState[0]][presentState[1]] = '_'
        presentState[1] = presentState[1] + 1

    elif direction == 'S' and presentState[0] + 1 < rMax and grid[presentState[0] + 1][presentState[1]] != "#":
        if grid[presentState[0]+1][presentState[1]] not in l:
            terminate = True
            finalReward = float(grid[presentState[0]+1][presentState[1]])
        totalLivingReward += float(livingReward)
        grid[presentState[0] + 1][presentState[1]] = 'P'
        grid[presentState[0]][presentState[1]] = '_'
        presentState[0] = presentState[0] + 1

    elif direction == 'W' and presentState[1] - 1 >= 0 and grid[presentState[0]][presentState[1] - 1] != "#":
        if grid[presentState[0]][presentState[1]-1] not in l:
            terminate = True
            finalReward = float(grid[presentState[0]][presentState[1]-1])
        totalLivingReward += float(livingReward)
        grid[presentState[0]][presentState[1] - 1] = 'P'
        grid[presentState[0]][presentState[1]] = '_'
        presentState[1] = presentState[1] - 1
    else:
        totalLivingReward += float(livingReward)

    return terminate, totalLivingReward, livingReward, finalReward

def getupdatedString(dir, intendedDir, reward, totalReward, grid, startState):
    string = f"Taking action: {dir} (intended: {intendedDir})\n" + f"Reward received: {reward}\n" + "New state:\n"
    for i, x in enumerate(grid):
        for k, y in enumerate(x):
            for j in range(5 - len(y)):
                string += " "
            if y == '_' and i == startState[0] and k == startState[1]:
                string += 'S'
            elif y == 'S' and i == startState[0] and k == startState[1]:
                string += 'P'
            else:
                string += y
        string += "\n"

    string += f"Cumulative reward sum: {totalReward}\n"
    string += "-------------------------------------------- \n"

    return string

def getInitialString(startState, startPosition):
    string = "Start state:\n"
    for i, x in enumerate(startState):
        for k, y in enumerate(x):
            for j in range(5 - len(y)):
                string += " "
            if i == startPosition[0] and k == startPosition[1]:
                string += "P"
            else:
                string += y
        string += "\n"
    string += "Cumulative reward sum: 0.0\n"
    string += "-------------------------------------------- \n"

    return string

def getExitString(reward, totalReward, grid, startState, currentState):
    string = "Taking action: exit (intended: exit)\n" + f"Reward received: {reward}\n" + "New state:\n"
    for i, x in enumerate(grid):
        for k, y in enumerate(x):
            if y == 'P':
                y = str(reward).split('.')[0] if str(reward).split('.')[1] == '0' else str(reward)
            for j in range(5 - len(y)):
                string += " "
            if y == '_' and i == startState[0] and k == startState[1]:
                string += 'S'
            else:
                string += y
        string += "\n"

    string += f"Cumulative reward sum: {totalReward}"

    return string


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)
