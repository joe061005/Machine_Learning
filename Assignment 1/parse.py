import os, sys
from heapq import heappush, heappop

def read_graph_search_problem(file_path):
    #Your p1 code here
    file = open(file_path)
    problem = {
        'startAndGoal': '',
        'heuristic': {},
        'state': {}
    }
    for i, line in enumerate(file):
        line = line.rstrip()
        if i == 0:
            problem['startAndGoal'] += line.split('start_state: ')[1] + " "
        elif i == 1:
            problem['startAndGoal'] += line.split('goal_states: ')[1]
        elif len(line.split(' ')) == 2:
            heuInfo = line.split(' ')
            problem['heuristic'][heuInfo[0]] = float(heuInfo[1])
        else:
            stateInfo = line.split(' ')
            if stateInfo[0] not in problem['state']:
                problem['state'][stateInfo[0]] = [(float(stateInfo[2]), stateInfo[1])]
            else:
                problem['state'][stateInfo[0]].append((float(stateInfo[2]), stateInfo[1]))

    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    file = open(file_path)
    #problem = {}
    # board = []
    queenList = {}

    for i, line in enumerate(file):
        line = line.strip().split(" ")
       # tempoList = []
        for i2, x in enumerate(line):
            if x == 'q':
               # tempoList.append('1')
                queenList[i2] = i
            #else:
              #  tempoList.append('0')
       # board.append(tempoList)

   # problem['board'] = board
   # problem['queenList'] = queenList

    return queenList

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')