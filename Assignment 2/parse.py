import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    problem = {
        'seed': 0,
        'layout': [],
        'pacLocation': [],
        'ghostLocation': {},
        'foodLocation': {},
        'ghostList': []
    }
    file = open(file_path)
    for i, line in enumerate(file):
        line = line.rstrip()
        tempList = []
        if i == 0:
            problem['seed'] = int(line.split(" ")[1])
        else:
            for j, char in enumerate(line):
                if char == '%':
                    tempList.append(char)
                else:
                    tempList.append(' ')

                if char == 'P':
                    problem['pacLocation'].append(i-1)
                    problem['pacLocation'].append(j)
                elif char == 'W' or char == 'X' or char == 'Y' or char == 'Z':
                    problem['ghostLocation'][char] = [i-1, j]
                    problem['ghostList'].append(char)
                elif char == '.':
                    problem['foodLocation'][f'{i-1} {j}'] = ''

            problem['layout'].append(tempList)

    problem['ghostList'].sort()
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')