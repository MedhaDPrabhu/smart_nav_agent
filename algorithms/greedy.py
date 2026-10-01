import heapq
import math

def euclidean_heuristic(u, v, coords):
    x1, y1 = coords[u]['x'], coords[u]['y']
    x2, y2 = coords[v]['x'], coords[v]['y']
    return math.hypot(x2 - x1, y2 - y1)

def greedy(graph, start, goal, coords, blocked_edges=None):
    blocked_edges = blocked_edges or set()
    # Priority Queue stores: (heuristic_h, path)
    pq = [(euclidean_heuristic(start, goal, coords), [start])]
    visited = set()
    nodes_expanded = 0

    while pq:
        h_val, path = heapq.heappop(pq)
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            cost = sum(graph[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))
            return path, cost, nodes_expanded

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if (node, neighbor) in blocked_edges or (neighbor, node) in blocked_edges:
                    continue
                new_h = euclidean_heuristic(neighbor, goal, coords)
                heapq.heappush(pq, (new_h, path + [neighbor]))

    return None, float('inf'), nodes_expanded