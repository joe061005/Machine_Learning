import sys, parse
import time, os, copy, random


def expecti_max_mulitple_ghosts(problem, k):
    # Your p6 code here
    if problem['seed'] != -1:
        random.seed(problem['seed'], version=1)
    round = 0
    score = 0
    solution = 'seed: ' + str(problem['seed']) + '\n'
    queue = ['P'] + problem['ghostList']
    agentDict = {
        'P': 0,
        'W': 1,
        'X': 2,
        'Y': 3,
        'Z': 4,
        0: 'P',
        1: 'W',
        2: 'X',
        3: 'Y',
        4: 'Z'
    }

    # len(problem['pacLocation']) > 0 and len(problem['foodLocation']) > 0

    while len(problem['pacLocation']) > 0 and len(problem['foodLocation']) > 0:
        if round == 0:
            solution = formatSolution(solution, round, problem['layout'], '', '', '', problem['pacLocation'],
                                      problem['ghostLocation'], problem['foodLocation'])
        else:
            character = queue.pop(0)
            queue.append(character)

            if character == 'P':
                tempFood = copy.deepcopy(problem['foodLocation'])
                tempPac = copy.deepcopy(problem['pacLocation'])
                tempGhost = copy.deepcopy(problem['ghostLocation'])
                direction = expectimax(agentDict[character], agentDict[character], problem['layout'], 0, k, len(queue),
                                    tempFood, tempPac, tempGhost, 0, agentDict)
                choice, score = Move(problem['pacLocation'], problem['ghostLocation'],
                                     problem['foodLocation'], score, direction)
            else:
                choice, score = MoveGhost(character, problem['layout'], problem['pacLocation'], problem['ghostLocation'], score)

            print(len(problem['foodLocation']))
            solution = formatSolution(solution, round, problem['layout'], character, choice, score,
                                      problem['pacLocation'], problem['ghostLocation'], problem['foodLocation'])

        round += 1

    solution += "WIN: Pacman" if len(problem['foodLocation']) == 0 else "WIN: Ghost"
    winner = "Pacman" if len(problem['foodLocation']) == 0 else "Ghost"

    return solution, winner


def expectimax(initialAgent, agent, layout, depth, maxDepth, maxAgent, foodLocation, pacLocation, ghostLocation, score,
            agentDict):

    if isLose(pacLocation) or isWin(foodLocation) or depth == maxDepth:
        return evaluationFunction(isLose(pacLocation), isWin(foodLocation), score, depth)

    newLocation = pacLocation if agent == 0 else ghostLocation[agentDict[agent]]

    avaDirDict = getAvailableDirections(agentDict[agent], layout, newLocation, ghostLocation)

    val_list = list(avaDirDict.values())

    if len(val_list) == 0 and depth == 0 and initialAgent == agent:
        return ''

    if agent == 0:
        maxValList = []
        for newLocation in val_list:
            tempFood = copy.deepcopy(foodLocation)
            tempPac = copy.deepcopy(pacLocation)
            tempGhost = copy.deepcopy(ghostLocation)
            tempScore = moveAndGetActionScores(agentDict[agent], newLocation, tempFood, tempPac, tempGhost, score)
            maxValList.append(
                expectimax(initialAgent, 1, layout, depth, maxDepth, maxAgent, tempFood, tempPac, tempGhost, tempScore,
                        agentDict))
        maxVal = max(maxValList)
        if initialAgent == agent and depth == 0:
            indexList = [i for i, val in enumerate(maxValList) if val == maxVal]
            key_list = list(avaDirDict.keys())
            index = random.choice(tuple(indexList))
            return key_list[index]
        return maxVal

    else:

        nextAgent = agent + 1
        if nextAgent == maxAgent:
            nextAgent = 0

        if nextAgent == 0:
            tempDepth = depth + 1
        else:
            tempDepth = depth

        chanceValList = []

        if len(val_list) == 0:
            tempFood = copy.deepcopy(foodLocation)
            tempPac = copy.deepcopy(pacLocation)
            tempGhost = copy.deepcopy(ghostLocation)
            chanceValList.append(
                expectimax(initialAgent, nextAgent, layout, tempDepth, maxDepth, maxAgent, tempFood, tempPac, tempGhost,
                        score, agentDict))
        else:
            for newLocation in val_list:
                tempFood = copy.deepcopy(foodLocation)
                tempPac = copy.deepcopy(pacLocation)
                tempGhost = copy.deepcopy(ghostLocation)
                tempScore = moveAndGetActionScores(agentDict[agent], newLocation, tempFood, tempPac, tempGhost, score)
                chanceValList.append(
                    expectimax(initialAgent, nextAgent, layout, tempDepth, maxDepth, maxAgent, tempFood, tempPac,
                            tempGhost, tempScore, agentDict))


        chanceVal = sum(chanceValList) / len(chanceValList)
        return chanceVal


def evaluationFunction(isLose, isWin, score, depth):
    if isLose:
        score -= 500
    elif isWin:
        score += 500

    return score


def moveAndGetActionScores(agent, newLocation, foodLocation, pacLocation, ghostLocation, score):
    if agent == 'P':
        if newLocation in ghostLocation.values():
            pacLocation.clear()
            score -= 1
        elif f"{newLocation[0]} {newLocation[1]}" in foodLocation:
            del foodLocation[f"{newLocation[0]} {newLocation[1]}"]
            pacLocation[0] = newLocation[0]
            pacLocation[1] = newLocation[1]
            score += 9
        else:
            pacLocation[0] = newLocation[0]
            pacLocation[1] = newLocation[1]
            score -= 1
    else:
        if newLocation[0] == pacLocation[0] and newLocation[1] == pacLocation[1]:
            pacLocation.clear()
            ghostLocation[agent] = [newLocation[0], newLocation[1]]
        else:
            ghostLocation[agent] = [newLocation[0], newLocation[1]]

    return score


def isLose(pacLocation):
    return len(pacLocation) == 0


def isWin(foodLocation):
    return len(foodLocation) == 0


def MoveGhost(character, layout, pacLocation, ghostLocation, score):
    choice, newLocation = getAvailableDirectionsForGhost(layout, ghostLocation[character], ghostLocation)

    if choice == '':
        return choice, score

    # The ghost eats the pacman
    if newLocation[0] == pacLocation[0] and newLocation[1] == pacLocation[1]:
        pacLocation.clear()
        ghostLocation[character] = [newLocation[0], newLocation[1]]
        score -= 500
    else:
        ghostLocation[character] = [newLocation[0], newLocation[1]]

    return choice, score


def Move(pacLocation, ghostLocation, foodLocation, score, choice):
    if choice == 'N':
        newLocation = [pacLocation[0] - 1, pacLocation[1]]
    elif choice == 'E':
        newLocation = [pacLocation[0], pacLocation[1] + 1]
    elif choice == 'S':
        newLocation = [pacLocation[0] + 1, pacLocation[1]]
    else:
        newLocation = [pacLocation[0], pacLocation[1] - 1]

    # it is eaten by the ghost
    if [newLocation[0], newLocation[1]] in ghostLocation.values():
        pacLocation.clear()
        score -= 501

    # it eats the food
    elif f"{newLocation[0]} {newLocation[1]}" in foodLocation:
        del foodLocation[f"{newLocation[0]} {newLocation[1]}"]
        pacLocation[0] = newLocation[0]
        pacLocation[1] = newLocation[1]
        score += 9
        if len(foodLocation) == 0:
            score += 500

    # it goes to an empty square
    else:
        pacLocation[0] = newLocation[0]
        pacLocation[1] = newLocation[1]
        score -= 1

    return choice, score


def getAvailableDirections(character, layout, location, ghostLocation):
    newLocationDir = {}

    # for pacman
    if character == 'P':
        # check E
        if layout[location[0]][location[1] + 1] != '%':
            newLocationDir['E'] = [location[0], location[1] + 1]
        # check N
        if layout[location[0] - 1][location[1]] != '%':
            newLocationDir['N'] = [location[0] - 1, location[1]]
        # check S
        if layout[location[0] + 1][location[1]] != '%':
            newLocationDir['S'] = [location[0] + 1, location[1]]
        # check W
        if layout[location[0]][location[1] - 1] != '%':
            newLocationDir['W'] = [location[0], location[1] - 1]


    # for ghost
    else:
        # check E
        if layout[location[0]][location[1] + 1] != '%' and [location[0], location[1] + 1] not in ghostLocation.values():
            newLocationDir['E'] = [location[0], location[1] + 1]
        # check N
        if layout[location[0] - 1][location[1]] != '%' and [location[0] - 1, location[1]] not in ghostLocation.values():
            newLocationDir['N'] = [location[0] - 1, location[1]]
        # check S
        if layout[location[0] + 1][location[1]] != '%' and [location[0] + 1, location[1]] not in ghostLocation.values():
            newLocationDir['S'] = [location[0] + 1, location[1]]
        # check W
        if layout[location[0]][location[1] - 1] != '%' and [location[0], location[1] - 1] not in ghostLocation.values():
            newLocationDir['W'] = [location[0], location[1] - 1]

    return newLocationDir


def getAvailableDirectionsForGhost(layout, location, ghostLocation):
    avaDir = []
    newLocationDir = {}

    # check E
    if layout[location[0]][location[1] + 1] != '%' and [location[0], location[1] + 1] not in ghostLocation.values():
        avaDir.append('E')
        newLocationDir['E'] = [location[0], location[1] + 1]
    # check N
    if layout[location[0] - 1][location[1]] != '%' and [location[0] - 1, location[1]] not in ghostLocation.values():
        avaDir.append('N')
        newLocationDir['N'] = [location[0] - 1, location[1]]
    # check S
    if layout[location[0] + 1][location[1]] != '%' and [location[0] + 1, location[1]] not in ghostLocation.values():
        avaDir.append('S')
        newLocationDir['S'] = [location[0] + 1, location[1]]
    # check W
    if layout[location[0]][location[1] - 1] != '%' and [location[0], location[1] - 1] not in ghostLocation.values():
        avaDir.append('W')
        newLocationDir['W'] = [location[0], location[1] - 1]

    if len(avaDir) > 0:
        choice = random.choice(tuple(avaDir))
        newLocation = newLocationDir[choice]
    else:
        choice = ''
        newLocation = []

    return choice, newLocation


def formatSolution(solution, round, layout, character, direction, score, pacLocation, ghostLocation, foodLocation):
    tempLayout = copy.deepcopy(layout)
    if round == 0:
        solution += f"{round}\n"
    elif direction == '':
        solution += f"{round}: {character} moving \n"
    else:
        solution += f"{round}: {character} moving {direction}\n"

    if len(pacLocation) > 0:
        tempLayout[pacLocation[0]][pacLocation[1]] = 'P'

    if len(foodLocation) > 0:
        for key in foodLocation.keys():
            location = key.split(' ')
            tempLayout[int(location[0])][int(location[1])] = '.'

    if len(ghostLocation) > 0:
        for key in ghostLocation.keys():
            val = ghostLocation[key]
            tempLayout[val[0]][val[1]] = key

    for x in tempLayout:
        solution += "".join(x) + "\n"

    solution += f"score: {score}\n" if round != 0 else ""
    return solution


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:', test_case_id)
    print('k:', k)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
