import sys, grader, parse, copy

def policy_evaluation(problem):
    sol = ''
    result = copy.deepcopy(problem['grid'])
    for x in range(problem['iteration']):
        sol += evaluate(x, problem['discount'], problem['noise'], problem['livingReward'], problem['grid'], problem['policy'], result)

    return sol.strip()

def evaluate(iteration, discount, noise, reward, grid, policy, result):
    notExit = ['_', 'S']
    string = f"V^pi_k={iteration}\n"
    if iteration == 0 or iteration == 1:
        for i, x in enumerate(grid):
            for j, y in enumerate(x):
                val = -999 if y == '#' else 0.00 if iteration == 0 else reward if y in notExit else y
                string += '|{:7.2f}|'.format(float(val)) if val != -999 else '| ##### |'
                result[i][j] = float(val)
            string += "\n"
    else:
       # d = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
        tempResult = copy.deepcopy(result)
        for i, x in enumerate(grid):
            for j, y in enumerate(x):
                if policy[i][j] == 'exit':
                    string += '|{:7.2f}|'.format(float(y))
                elif policy[i][j] == '#':
                    string += '| ##### |'
                else:
                    total = 0
                    if policy[i][j] == 'N':
                        if i-1 >= 0 and policy[i-1][j] != '#':
                            total += (1-noise*2)*(discount*tempResult[i-1][j]+reward)
                        else:
                            total += (1 - noise * 2) * (discount * tempResult[i][j] + reward)

                        if j + 1 < len(tempResult[0]) and policy[i][j+1] != '#':
                            total += noise * (discount * tempResult[i][j+1] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)

                        if j - 1 >= 0 and policy[i][j-1] != '#':
                            total += noise * (discount * tempResult[i][j - 1] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)
                    elif policy[i][j] == 'E':
                        if j + 1 < len(tempResult[0]) and policy[i][j+1] != '#':
                            total += (1-noise*2) * (discount * tempResult[i][j + 1] + reward)
                        else:
                            total += (1-noise*2) * (discount * tempResult[i][j] + reward)

                        if i + 1 < len(tempResult) and policy[i+1][j] != '#':
                            total += noise * (discount * tempResult[i + 1][j] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)

                        if i-1 >= 0 and policy[i-1][j] != '#':
                            total += noise * (discount * tempResult[i - 1][j] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)

                    elif policy[i][j] == 'S':
                        if i + 1 < len(tempResult) and policy[i+1][j] != '#':
                            total += (1-noise*2) * (discount * tempResult[i + 1][j] + reward)
                        else:
                            total += (1-noise*2) * (discount * tempResult[i][j] + reward)

                        if j - 1 >= 0 and policy[i][j-1] != '#':
                            total += noise * (discount * tempResult[i][j - 1] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)

                        if j + 1 < len(tempResult[0]) and policy[i][j+1] != '#':
                            total += noise * (discount * tempResult[i][j + 1] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)
                    else:
                        if j - 1 >= 0 and policy[i][j-1] != '#':
                            total += (1-noise*2) * (discount * tempResult[i][j - 1] + reward)
                        else:
                            total += (1-noise*2) * (discount * tempResult[i][j] + reward)

                        if i-1 >= 0 and policy[i-1][j] != '#':
                            total += noise * (discount * tempResult[i - 1][j] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)

                        if i + 1 < len(tempResult) and policy[i+1][j] != '#':
                            total += noise * (discount * tempResult[i + 1][j] + reward)
                        else:
                            total += noise * (discount * tempResult[i][j] + reward)
                    result[i][j] = total
                    string += '|{:7.2f}|'.format(float(total))
            string += "\n"

    return string



if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)