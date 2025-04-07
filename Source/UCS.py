import queue
import enum
from collections import deque

class V(enum.Enum):
    NOT_VISITED = 0
    FRONTIER = 1
    EXPLORED = 2

def ucs(graph, start, goal):
    visited = dict()
    for state in graph:
        visited[state] = V.NOT_VISITED

    node = (start, None, 0)
    frontier = queue.PriorityQueue()
    explored = []

    frontier.put((0, node))
    visited[start] = V.FRONTIER

    while not frontier.empty():
        current_cost, node = frontier.get()
        explored.append((node[0], node[1], current_cost))
        visited[node[0]] = V.EXPLORED

        if node[0] == goal:
            return get_path(explored)

        for child, edge_cost in graph[node[0]]:
            if visited[child] == V.NOT_VISITED:
                new_cost = current_cost + edge_cost
                frontier.put((new_cost, (child, node[0], new_cost)))
                visited[child] = V.FRONTIER

    return None

def get_path(explored):
    parent_table = dict()
    for state, parent, cost in explored:
        parent_table[state] = parent

    state = explored[-1][0]
    path = deque([state])
    parent = parent_table[state]

    while parent is not None:
        path.appendleft(parent)
        parent = parent_table[parent]

    return list(path)
