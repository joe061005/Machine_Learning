import sys, random, grader, parse, copy


def random_play_single_ghost(problem):
    # Your p1 code here
    # N E S W -> E N S W
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

    return solution


def Move(character, layout, pacLocation, ghostLocation, foodLocation, score):
    location = pacLocation if character == 'P' else ghostLocation[character]
    choice, newLocation = getAvailableDirections(character, layout, location, ghostLocation)

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


def getAvailableDirections(character, layout, location, ghostLocation):
    avaDir = []
    newLocationDir = {}

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

    choice = random.choice(tuple(avaDir))
    newLocation = newLocationDir[choice]

    return choice, newLocation


def formatSolution(solution, round, layout, character, direction, score, pacLocation, ghostLocation, foodLocation):
    tempLayout = copy.deepcopy(layout)
    solution += f"{round}\n" if round == 0 else f"{round}: {character} moving {direction}\n"
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
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)
