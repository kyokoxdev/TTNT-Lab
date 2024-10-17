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
        heap = [(self.heuristic[start], start, [start])]
        visited = set()

        while heap:
            current_cost, current_node, path = heapq.heappop(heap)

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == goal:
                return path, current_cost

            for neighbor, cost in self.graph.get(current_node, []):
                if neighbor not in visited:
                    new_cost = current_cost - self.heuristic[current_node] + cost + self.heuristic[neighbor]
                    heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

        return None, float('inf')

def main():
    graph = Graph()
    edges = int(input("Nhập số lượng cạnh: "))
    print("Nhập từng cạnh theo syntax: start target cost")
    for _ in range(edges):
        startpoint, endpoint, cost = input().split()
        cost = float(cost)
        graph.add_edge(startpoint, endpoint, cost)