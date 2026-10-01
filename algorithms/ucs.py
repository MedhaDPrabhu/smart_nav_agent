import heapq

def ucs(graph, start, goal, blocked_edges=None):
    blocked_edges = blocked_edges or set()
    # Priority Queue stores: (cumulative_cost_g, path)
    pq = [(0, [start])]
    visited = {}
    nodes_expanded = 0

    while pq:
        g_val, path = heapq.heappop(pq)
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
            heapq.heappush(pq, (new_g, path + [neighbor]))

    return None, float('inf'), nodes_expanded