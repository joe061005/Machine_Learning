import sys, parse, grader
from heapq import heappush, heappop

def greedy_search(problem):
    #Your p4 code here
    stateSpaceGraph = problem['state']
    heuristicDict = problem['heuristic']
    startState = problem['startAndGoal'].split(' ')[0]
    goalState = problem['startAndGoal'].split(' ')[1]

    frontier = []
    heappush(frontier, (heuristicDict[startState], startState))
    exploredSet = set()
    order = []

    while frontier:
        node = heappop(frontier)
        if node[1].endswith(goalState):
            break

        newNode = node[1].split(" ")[-1]
        if newNode not in exploredSet:
            exploredSet.add(newNode)
            order.append(newNode)
            if newNode in stateSpaceGraph:
                for child in stateSpaceGraph[newNode]:
                    heappush(frontier, (heuristicDict[child[1]], node[1] + " " + child[-1]))

    return " ".join(order) + '\n' + node[1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)