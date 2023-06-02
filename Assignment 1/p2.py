import sys, grader, parse
import collections

def bfs_search(problem):
    #Your p2 code here
    stateSpaceGraph = problem['state']
    startState = problem['startAndGoal'].split(' ')[0]
    goalState = problem['startAndGoal'].split(' ')[1]

    frontier = collections.deque([startState])
    exploredSet = set()
    order = []

    while frontier:
        node = frontier.popleft()
        if node.endswith(goalState):
            break

        newNode = node.split(" ")[-1]
        if newNode not in exploredSet:
            exploredSet.add(newNode)
            order.append(newNode)
            if newNode in stateSpaceGraph:
                for child in stateSpaceGraph[newNode]:
                    frontier.append(node + " " + child[-1])

    return " ".join(order) + '\n' + node

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)