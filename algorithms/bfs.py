from collections import deque

def bfs(graph, start, goal, blocked_edges=None):
    blocked_edges = blocked_edges or set()
    queue = deque([[start]])
    visited = set()
    nodes_expanded = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_expanded += 1

        if node == goal:
            cost = calculate_path_cost(graph, path)
            return path, cost, nodes_expanded

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if (node, neighbor) in blocked_edges or (neighbor, node) in blocked_edges:
                    continue
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None, float('inf'), nodes_expanded

def calculate_path_cost(graph, path):
    return sum(graph[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))