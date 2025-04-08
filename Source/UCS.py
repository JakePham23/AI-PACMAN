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
    
    # Trong UCS, node bao gồm (state, parent, cost_so_far)
    node = (start, None, 0)
    # PriorityQueue sắp xếp theo chi phí
    frontier = queue.PriorityQueue()
    explored = []
    
    # Đưa vào frontier với ưu tiên là chi phí
    frontier.put((0, node))  # (priority, node)
    visited[start] = V.FRONTIER
    
    # Theo dõi chi phí tốt nhất đến mỗi trạng thái
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        # Lấy nút có chi phí thấp nhất
        priority, node = frontier.get()
        state, parent, cost = node
        
        # Nếu trạng thái đã được khám phá với chi phí thấp hơn, bỏ qua
        if visited[state] == V.EXPLORED:
            continue
        
        explored.append((state, parent))
        visited[state] = V.EXPLORED
        
        if state == goal:
            return get_path(explored)  # success
        
        for child in graph[state]:
            # Tính chi phí mới
            # Giả định mặc định mỗi bước chi phí = 1
            # Trong trường hợp thực tế, bạn cần thay đổi 1 thành graph[state][child]
            new_cost = cost + 1
            
            # Nếu chưa từng thăm hoặc tìm thấy đường đi tốt hơn
            if visited[child] != V.EXPLORED and (child not in cost_so_far or new_cost < cost_so_far[child]):
                cost_so_far[child] = new_cost
                frontier.put((new_cost, (child, state, new_cost)))
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