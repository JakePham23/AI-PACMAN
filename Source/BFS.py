import queue
import enum
from collections import deque

class V(enum.Enum):
    NOT_VISITED = 0
    FRONTIER = 1
    EXPLORED = 2

def bfs(graph, start, goal):
    visited = dict()
    for state in graph:
        visited[state] = V.NOT_VISITED

    node = (start, None)  # node = (state, parent)
    frontier = queue.Queue()
    explored = []

    frontier.put(node)
    visited[start] = V.FRONTIER

    while not frontier.empty():
        node = frontier.get()
        explored.append((node[0], node[1]))
        visited[node[0]] = V.EXPLORED

        if node[0] == goal:
            return get_path(explored)  # success

        for child in graph[node[0]]:
            if visited[child] == V.NOT_VISITED:
                frontier.put((child, node[0]))
                visited[child] = V.FRONTIER

    return None  # failure

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
