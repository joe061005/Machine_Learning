import sys, parse
import time, os, copy, random, math

def better_play_mulitple_ghosts(problem):
    #Your p4 code here
    if problem['seed'] != -1:
        random.seed(problem['seed'], version=1)
    round = 0
    score = 0
    solution = 'seed: ' + str(problem['seed']) + '\n'
    queue = ['P'] + problem['ghostList']

    # len(problem['pacLocation']) > 0 and len(problem['foodLocation']) > 0

    while len(problem['pacLocation']) > 0 and len(problem['foodLocation']) > 0:
        if round == 0:
            solution = formatSolution(solution, round, problem['layout'], '', '', '', problem['pacLocation'],
                                      problem['ghostLocation'], problem['foodLocation'])
        else:
            character = queue.pop(0)
            queue.append(character)
            choice, score = Move(character, problem['layout'], problem['pacLocation'], problem['ghostLocation'],
                                 problem['foodLocation'], score)
            solution = formatSolution(solution, round, problem['layout'], character, choice, score,
                                      problem['pacLocation'], problem['ghostLocation'], problem['foodLocation'])

        round += 1

    solution += "WIN: Pacman" if len(problem['foodLocation']) == 0 else "WIN: Ghost"
    winner = "Pacman" if len(problem['foodLocation']) == 0 else "Ghost"
    return solution, winner

def Move(character, layout, pacLocation, ghostLocation, foodLocation, score):
    location = pacLocation if character == 'P' else ghostLocation[character]
    choice, newLocation = getAvailableDirections(character, layout, location, ghostLocation, foodLocation)

    if choice == '':
        return choice, score

    if character == 'P':

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

    else:

        # The ghost eats the pacman
        if newLocation[0] == pacLocation[0] and newLocation[1] == pacLocation[1]:
            pacLocation.clear()
            ghostLocation[character] = [newLocation[0], newLocation[1]]
            score -= 500
        else:
            ghostLocation[character] = [newLocation[0], newLocation[1]]


    return choice, score


def getAvailableDirections(character, layout, location, ghostLocation, foodLocation):
    avaDir = []
    newLocationDir = {}

    # for pacman
    if character == 'P':
        # check E
        if layout[location[0]][location[1] + 1] != '%':
            avaDir.append('E')
            newLocationDir['E'] = [location[0], location[1] + 1]
        # check N
        if layout[location[0] - 1][location[1]] != '%':
            avaDir.append('N')
            newLocationDir['N'] = [location[0] - 1, location[1]]
        # check S
        if layout[location[0] + 1][location[1]] != '%':
            avaDir.append('S')
            newLocationDir['S'] = [location[0] + 1, location[1]]
        # check W
        if layout[location[0]][location[1] - 1] != '%':
            avaDir.append('W')
            newLocationDir['W'] = [location[0], location[1] - 1]

        choice = evaluateBetterPosition(newLocationDir, ghostLocation, foodLocation)
        newLocation = newLocationDir[choice] if choice in newLocationDir else location


    # for ghost
    else:
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

def evaluateBetterPosition(newLocationDir, ghostLocation, foodLocation):
    direction = ''
    score = 0
    firstEle = True
    for key in newLocationDir.keys():
        position = newLocationDir[key]
        minGhostDistance = min([math.dist(x, position) for x in ghostLocation.values()])
        sortedFoodDistance = sorted([math.dist([int(x.split(" ")[0]), int(x.split(" ")[1])], position) for x in foodLocation.keys()])
        if sortedFoodDistance[0] == minGhostDistance and len(sortedFoodDistance) > 1:
            minFoodDistance = sortedFoodDistance[1]
        elif sortedFoodDistance[0] == 0:
            minFoodDistance = 1
        else:
            minFoodDistance = sortedFoodDistance[0]

        if minGhostDistance <= 1:
            tempScore = minGhostDistance * -50 + 1 / minFoodDistance
        else:
            tempScore = minGhostDistance + 1 / minFoodDistance * 50

        if firstEle:
            score = tempScore
            direction = key
            firstEle = False
        else:
            if tempScore > score:
                direction = key
                score = tempScore


    return direction



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
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)