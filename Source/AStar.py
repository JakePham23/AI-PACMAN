import heapq
import enum
from collections import deque

class V(enum.Enum):
    NOT_VISITED = 0
    FRONTIER = 1
    EXPLORED = 2

def heuristic(a, b):
    # Heuristic: khoảng cách Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(graph, start, goal):
    visited = dict()
    for state in graph:
        visited[state] = V.NOT_VISITED

    frontier = []
    heapq.heappush(frontier, (0 + heuristic(start, goal), 0, (start, None)))  # (f = g + h, g, (state, parent))
    explored = []

    visited[start] = V.FRONTIER

    while frontier:
        f, g, node = heapq.heappop(frontier)
        explored.append((node[0], node[1]))
        visited[node[0]] = V.EXPLORED

        if node[0] == goal:
            return get_path(explored), len(explored)

        for child in graph[node[0]]:
            if visited[child] == V.NOT_VISITED:
                heapq.heappush(frontier, (g + 1 + heuristic(child, goal), g + 1, (child, node[0])))
                visited[child] = V.FRONTIER

    return None, len(explored)

def get_path(explored):
    parent_table = dict()
    for state, parent in explored:
        parent_table[state] = parent

    state = explored[-1][0]
    path = deque([state])
    parent = parent_table[state]

    while parent is not None:
        path.appendleft(parent)
        parent = parent_table[parent]

    return list(path)
