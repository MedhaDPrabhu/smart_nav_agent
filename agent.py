import time
from algorithms.bfs import bfs
from algorithms.ucs import ucs
from algorithms.greedy import greedy
from algorithms.astar import astar

class CampusAgent:
    def __init__(self, graph_dict, coords):
        self.coords = coords
        self.graph = self._build_adj_list(graph_dict)

    def _build_adj_list(self, graph_dict):
        adj = {node: {} for node in self.coords}
        for edge in graph_dict['edges']:
            u, v, w = edge['from'], edge['to'], edge['weight']
            adj[u][v] = {'weight': w}
            adj[v][u] = {'weight': w}
        return adj

    def find_route(self, start, goal, algo_name, blocked_edges):
        start_time = time.perf_counter()
        
        if algo_name == "BFS":
            path, cost, expanded = bfs(self.graph, start, goal, blocked_edges)
        elif algo_name == "UCS":
            path, cost, expanded = ucs(self.graph, start, goal, blocked_edges)
        elif algo_name == "Greedy Best-First":
            path, cost, expanded = greedy(self.graph, start, goal, self.coords, blocked_edges)
        elif algo_name == "A* Search":
            path, cost, expanded = astar(self.graph, start, goal, self.coords, blocked_edges)
        else:
            path, cost, expanded = None, float('inf'), 0
            
        elapsed_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
        
        return {
            "algorithm": algo_name,
            "path": path,
            "cost": cost,
            "expanded": expanded,
            "time_ms": round(elapsed_time, 3)
        }