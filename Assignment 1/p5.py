import sys, parse, grader
from heapq import heappush, heappop


def astar_search(problem):
    # Your p5 code here
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
                    heappush(frontier, (
                    node[0] + child[0] + heuristicDict[child[1]] - heuristicDict[newNode],
                    node[1] + " " + child[-1]))

    return " ".join(order) + '\n' + node[1]


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)
