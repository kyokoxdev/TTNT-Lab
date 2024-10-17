import heapq

class Graph:
    def graph_init(self):
        self.graph = {}
        self.heuristic = {}
    def add_edge(self, startpoint, endpoint, cost):
        if startpoint not in self.graph:
            self.graph[startpoint] = []
        self.graph[startpoint].append((endpoint, cost))
    def set_heuristic(self, node, value):
        self.heuristic[node] = value
    def bnb_algorithm(self, start, goal):
        
    