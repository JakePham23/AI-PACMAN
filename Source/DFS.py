import enum
from collections import deque

class V(enum.Enum):
    NOT_VISITED = 0
    FRONTIER = 1
    EXPLORED = 2

def dfs(graph, start, goal):

    # Khởi tạo trạng thái của tất cả các node trong đồ thị
    visited = {state: V.NOT_VISITED for state in graph}
    # Stack lưu các tuple (node hiện tại, parent)
    stack = [(start, None)]
    # Đánh dấu node start đang ở trạng thái FRONTIER
    visited[start] = V.FRONTIER
    # Lưu lại thông tin duyệt để tái tạo đường đi
    explored = []

    while stack:
        node, parent = stack.pop()
        explored.append((node, parent))
        visited[node] = V.EXPLORED

        if node == goal:
            return get_path(explored)

        # Duyệt các node kề của node hiện tại
        for child in graph.get(node, []):
            if visited[child] == V.NOT_VISITED:
                stack.append((child, node))
                # Đánh dấu child là trong state FRONTIER ngay khi thêm vào stack
                visited[child] = V.FRONTIER

    return None  # Trả về None nếu không tìm thấy đường đi

def get_path(explored):
    if not explored:
        return []

    # Xây dựng bảng parent cho từng node
    parent_table = {}
    for state, parent in explored:
        parent_table[state] = parent

    # Lấy node đích từ phần tử cuối cùng của explored
    goal = explored[-1][0]
    path = []
    current = goal

    # Truy vết ngược từ goal về start theo bảng parent
    while current is not None:
        path.append(current)
        current = parent_table.get(current)
    path.reverse()
    return path
