import sys, grader, parse, copy


def value_iteration(problem):
    sol = ''
    policy = copy.deepcopy(problem['grid'])
    for x in range(problem['iteration']):
        sol += evaluate(x, problem['discount'], problem['noise'], problem['livingReward'], problem['grid'], policy)


    return sol.strip()


def evaluate(iteration, discount, noise, reward, grid, policy):
    string = f"V_k={iteration}\n"
    notExit = ['_', 'S']
    if iteration == 0 or iteration == 1:
        tempGrid = copy.deepcopy(grid)
        for i, x in enumerate(grid):
            for j, y in enumerate(x):
                val = -999 if y == '#' else 0.00 if iteration == 0 else reward if y in notExit else y
                string += '|{:7.2f}|'.format(float(val)) if val != -999 else '| ##### |'
                policy[i][j] = '#' if y == '#' else 'x' if y not in notExit else 'N'
                tempGrid[i][j] = float(val) if val != -999 else '#'
            string += "\n"

        if iteration == 1:
            for i, x in enumerate(tempGrid):
                for j, y in enumerate(x):
                    grid[i][j] = tempGrid[i][j]

    else:
        # d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
        tempGrid = copy.deepcopy(grid)
        for i, x in enumerate(grid):
            for j, y in enumerate(x):
                if policy[i][j] == 'x':
                    string += '|{:7.2f}|'.format(float(y))
                    tempGrid[i][j] = grid[i][j]
                elif policy[i][j] == '#':
                    string += '| ##### |'
                    tempGrid[i][j] = '#'
                else:
                    valArr = []
                    for num in range(4):
                        total = 0
                        # N
                        if num == 0:
                            if i - 1 >= 0 and grid[i - 1][j] != '#':
                                total += (1 - noise * 2) * (discount * grid[i - 1][j] + reward)
                            else:
                                total += (1 - noise * 2) * (discount * grid[i][j] + reward)

                            if j + 1 < len(grid[0]) and grid[i][j + 1] != '#':
                                total += noise * (discount * grid[i][j + 1] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)

                            if j - 1 >= 0 and grid[i][j - 1] != '#':
                                total += noise * (discount * grid[i][j - 1] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)
                        # E
                        elif num == 1:
                            if j + 1 < len(grid[0]) and grid[i][j + 1] != '#':
                                total += (1 - noise * 2) * (discount * grid[i][j + 1] + reward)
                            else:
                                total += (1 - noise * 2) * (discount * grid[i][j] + reward)

                            if i + 1 < len(grid) and grid[i + 1][j] != '#':
                                total += noise * (discount * grid[i + 1][j] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)

                            if i - 1 >= 0 and grid[i - 1][j] != '#':
                                total += noise * (discount * grid[i - 1][j] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)
                        # S
                        elif num == 2:
                            if i + 1 < len(grid) and grid[i + 1][j] != '#':
                                total += (1 - noise * 2) * (discount * grid[i + 1][j] + reward)
                            else:
                                total += (1 - noise * 2) * (discount * grid[i][j] + reward)

                            if j - 1 >= 0 and grid[i][j - 1] != '#':
                                total += noise * (discount * grid[i][j - 1] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)

                            if j + 1 < len(grid[0]) and grid[i][j + 1] != '#':
                                total += noise * (discount * grid[i][j + 1] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)
                        # w
                        else:
                            if j - 1 >= 0 and grid[i][j - 1] != '#':
                                total += (1 - noise * 2) * (discount * grid[i][j - 1] + reward)
                            else:
                                total += (1 - noise * 2) * (discount * grid[i][j] + reward)

                            if i - 1 >= 0 and grid[i - 1][j] != '#':
                                total += noise * (discount * grid[i - 1][j] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)

                            if i + 1 < len(grid) and grid[i + 1][j] != '#':
                                total += noise * (discount * grid[i + 1][j] + reward)
                            else:
                                total += noise * (discount * grid[i][j] + reward)
                        valArr.append(total)
                    if valArr.count(max(valArr)) != 4:
                        idx = valArr.index(max(valArr))
                        tempGrid[i][j] = max(valArr)
                        policy[i][j] = 'N' if idx == 0 else 'E' if idx == 1 else 'S' if idx == 2 else 'W'
                    else:
                        tempGrid[i][j] = max(valArr)
                    string += '|{:7.2f}|'.format(float(tempGrid[i][j]))

            string += "\n"
        for i, x in enumerate(tempGrid):
            for j, y in enumerate(x):
                grid[i][j] = tempGrid[i][j]

    if iteration > 0:
        string += f"pi_k={iteration}\n"
        for i, x in enumerate(policy):
            for j, y in enumerate(x):
                string += f'| {y} |'
            string += "\n"

    return string


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)
