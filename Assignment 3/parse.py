def read_grid_mdp_problem_p1(file_path):
    # Your p1 code here
    problem = {
        'seed': 0,
        'noise': 0,
        'livingReward': 0,
        'grid': {},
        'policy': {},
        'state': [],
        'present': []
    }
    file = open(file_path)
    isgrid = True
    gridList = []
    policyList = []
    for i, line in enumerate(file):
        line = line.rstrip()
        if i == 0:
            problem['seed'] = int(line.split(" ")[1])
        elif i == 1:
            problem['noise'] = float(line.split(" ")[1])
        elif i == 2:
            problem['livingReward'] = float(line.split(" ")[1])
        else:
            if line == "policy:":
                isgrid = False
                continue
            elif line == "grid:":
                continue

            tempList = []
            for j, char in enumerate(line.split()):
                tempList.append(char)
            if isgrid:
                gridList.append(tempList)
            else:
                policyList.append(tempList)

    problem['grid'] = gridList
    problem['policy'] = policyList

    for i, row in enumerate(gridList):
        for j, col in enumerate(row):
            if col == 'S':
                problem['state'] = [i, j]
                problem['present'] = [i, j]
                return problem

    return problem


def read_grid_mdp_problem_p2(file_path):
    # Your p2 code here
    problem = {
        'discount': 0,
        'noise': 0,
        'livingReward': 0,
        'iteration': 0,
        'grid': {},
        'policy': {},
    }
    file = open(file_path)
    isgrid = True
    gridList = []
    policyList = []
    for i, line in enumerate(file):
        line = line.rstrip()
        if i == 0:
            problem['discount'] = float(line.split(" ")[1])
        elif i == 1:
            problem['noise'] = float(line.split(" ")[1])
        elif i == 2:
            problem['livingReward'] = float(line.split(" ")[1])
        elif i == 3:
            problem['iteration'] = int(line.split(" ")[1])
        else:
            if line == "policy:":
                isgrid = False
                continue
            elif line == "grid:":
                continue

            tempList = []
            for j, char in enumerate(line.split()):
                tempList.append(char)
            if isgrid:
                gridList.append(tempList)
            else:
                policyList.append(tempList)

    problem['grid'] = gridList
    problem['policy'] = policyList


    return problem


def read_grid_mdp_problem_p3(file_path):
    # Your p3 code here
    problem = {
        'discount': 0,
        'noise': 0,
        'livingReward': 0,
        'iteration': 0,
        'grid': {},
    }
    file = open(file_path)
    gridList = []
    for i, line in enumerate(file):
        line = line.rstrip()
        if i == 0:
            problem['discount'] = float(line.split(" ")[1])
        elif i == 1:
            problem['noise'] = float(line.split(" ")[1])
        elif i == 2:
            problem['livingReward'] = float(line.split(" ")[1])
        elif i == 3:
            problem['iteration'] = int(line.split(" ")[1])
        else:
            if line == "grid:":
                continue
            tempList = []
            for j, char in enumerate(line.split()):
                tempList.append(char)
            gridList.append(tempList)

    problem['grid'] = gridList

    return problem
