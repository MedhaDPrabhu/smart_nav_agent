import heapq
import math

def euclidean_heuristic(u, v, coords):
    x1, y1 = coords[u]['x'], coords[u]['y']
    x2, y2 = coords[v]['x'], coords[v]['y']
    return math.hypot(x2 - x1, y2 - y1)

def astar(graph, start, goal, coords, blocked_edges=None):
    blocked_edges = blocked_edges or set()
    # Priority Queue stores: (f_val, g_val, path)
    pq = [(0 + euclidean_heuristic(start, goal, coords), 0, [start])]
    visited = {}
    nodes_expanded = 0

    while pq:
        f_val, g_val, path = heapq.heappop(pq)
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            return path, g_val, nodes_expanded

        if node in visited and visited[node] <= g_val:
            continue
        visited[node] = g_val

        for neighbor, data in graph[node].items():
            if (node, neighbor) in blocked_edges or (neighbor, node) in blocked_edges:
                continue
            new_g = g_val + data['weight']
            new_f = new_g + euclidean_heuristic(neighbor, goal, coords)
            heapq.heappush(pq, (new_f, new_g, path + [neighbor]))

    return None, float('inf'), nodes_expanded