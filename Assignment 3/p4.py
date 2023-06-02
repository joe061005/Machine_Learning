import random

import parse, copy


# simply run this program
# This program cannot always get the optimal policy, it is because there is noise effect is not large in this setting
# For example, at row 2, column 3, sometimes the agent would move upwards (N) and get positive reward because of small noise effect
# In other words, as it seldom moves to the east, the reward of moving upwards (N) is larger than other actions (E, S, W)
# this may affect the operation of other neighbours, so the policy may not be always optimal
# around 50% probability to get the optimal policy

def startQLearning():
    alpha = 0.5
    epsilon = 0.5
    problem = parse.read_grid_mdp_problem_p3('./test_cases/p3/2.prob')
    QGrid = copy.deepcopy(problem['grid'])
    policy = copy.deepcopy(problem['grid'])
    for i, x in enumerate(problem['grid']):
        for j, y in enumerate(x):
            QGrid[i][j] = {'N': 0, 'E': 0, 'S': 0, 'W': 0} if y == '_' or y == 'S' else None if y == '#' else int(y)
            policy[i][j] = '' if y == '_' or y == 'S' else '#' if y == '#' else int(y)
    iteration = 0
    optimalSolution = [['E', 'E', 'E', 1], ['N', '#', 'W', -1], ['N', 'W', 'W', 'S']]

    while iteration < 100:

        for i, x in enumerate(QGrid):
            for j, y in enumerate(x):
                if type(y) is not dict:
                    continue

                explore = random.choices(population=[True, False], weights=[epsilon, 1 - epsilon])

                if explore[0]:
                    choices = [x for x in y.keys() if y[x] != max(y.values())] if max(y.values()) != 0 else ['N', 'E',
                                                                                                             'S', 'W']
                else:
                    choices = [x for x in y.keys() if y[x] == max(y.values())]

                if len(choices) == 0:
                    choices = ['N', 'E', 'S', 'W']
                choice = random.choice(choices) if len(choices) > 1 else choices[0]

                if choice == 'N':
                    actChoice = random.choices(population=['N', 'E', 'W'],
                                               weights=[1 - problem['noise'] * 2, problem['noise'], problem['noise']])[
                        0]
                elif choice == 'E':
                    actChoice = random.choices(population=['E', 'S', 'N'],
                                               weights=[1 - problem['noise'] * 2, problem['noise'], problem['noise']])[
                        0]
                elif choice == 'S':
                    actChoice = random.choices(population=['S', 'W', 'E'],
                                               weights=[1 - problem['noise'] * 2, problem['noise'], problem['noise']])[
                        0]
                else:
                    actChoice = random.choices(population=['W', 'N', 'S'],
                                               weights=[1 - problem['noise'] * 2, problem['noise'], problem['noise']])[
                        0]

                if actChoice == 'N':
                    if i - 1 >= 0:
                        maxQ = max(QGrid[i - 1][j].values()) if type(QGrid[i - 1][j]) is dict else QGrid[i - 1][
                            j] if type(QGrid[i - 1][j]) is int else 0
                    else:
                        maxQ = 0

                elif actChoice == 'E':
                    if j + 1 < len(QGrid[0]):
                        maxQ = max(QGrid[i][j + 1].values()) if type(QGrid[i][j + 1]) is dict else QGrid[i][
                            j + 1] if type(QGrid[i][j + 1]) is int else 0
                    else:
                        maxQ = 0

                elif actChoice == 'S':
                    if i + 1 < len(QGrid):
                        maxQ = max(QGrid[i + 1][j].values()) if type(QGrid[i + 1][j]) is dict else QGrid[i + 1][
                            j] if type(QGrid[i + 1][j]) is int else 0
                    else:
                        maxQ = 0

                elif actChoice == 'W':
                    if j - 1 >= 0:
                        maxQ = max(QGrid[i][j - 1].values()) if type(QGrid[i][j - 1]) is dict else QGrid[i][
                            j - 1] if type(QGrid[i][j - 1]) is int else 0
                    else:
                        maxQ = 0

                if maxQ != 0:
                    sample = problem['livingReward'] + problem['discount'] * maxQ
                    QGrid[i][j][choice] = (1 - alpha) * y[choice] + alpha * sample

                if max(QGrid[i][j].values()) != 0:
                    maxDir = []
                    for ky in QGrid[i][j].keys():
                        if y[ky] == max(QGrid[i][j].values()):
                            maxDir.append(ky)
                    policy[i][j] = maxDir[0] if len(maxDir) == 1 else ''

        iteration += 1
        epsilon -= random.uniform(0.001, 0.004)
        alpha -= random.uniform(0.001, 0.004)


    string = ""

    for x in policy:
        for y in x:
            for s in range(5 - len(str(y))):
                string += " "
            string += str(y)
        string += "\n"

    print(string)


if __name__ == "__main__":
    startQLearning()
