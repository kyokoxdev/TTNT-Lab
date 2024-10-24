import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = {}
        self.heuristic = {}

    def add_edge(self, from_node, to_node, cost):
        if from_node not in self.graph:
            self.graph[from_node] = []
        self.graph[from_node].append((to_node, cost))

    def set_heuristic(self, node, h_value):
        self.heuristic[node] = h_value

    def branch_and_bound(self, start, goal):
        heap = [(self.heuristic[start], start, [start])]  
        visited = set()
        traversal_process = []  

        while heap:
            current_cost, current_node, path = heapq.heappop(heap)

            if current_node in visited:
                continue

            visited.add(current_node)
            traversal_process.append(current_node)  

            if current_node == goal:
                return path, current_cost, traversal_process

            for neighbor, cost in self.graph.get(current_node, []):
                if neighbor not in visited:
                    new_cost = current_cost - self.heuristic[current_node] + cost + self.heuristic[neighbor]
                    heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

        return None, float('inf'), traversal_process

    def draw_graph_with_arrows(self, path):
        G = nx.DiGraph()

        # Add edges from the graph with weights
        for from_node in self.graph:
            for to_node, cost in self.graph[from_node]:
                G.add_edge(from_node, to_node, weight=cost)

        # Use spring layout with increased k value for more spacing between nodes
        pos = nx.spring_layout(G, k=1.2, seed=42)

        # Draw the graph with larger nodes, thicker edges, and adjusted font size for readability
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=5000, font_size=14, font_weight='bold')

        # Draw edge labels with larger font
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

        # Highlight the found path with arrows and nodes in yellow
        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, arrowstyle='->', arrowsize=20)
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='yellow', node_size=5000)

        plt.title("Branch and Bound Found Path (With Arrows)")
        plt.show()


def main():
    graph = Graph()
   
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        from_node, to_node, cost, heuristic_start, heuristic_goal = line.split()
        cost = float(cost)
        heuristic_start = float(heuristic_start)
        heuristic_goal = float(heuristic_goal)
        
        graph.add_edge(from_node, to_node, cost)
        graph.set_heuristic(from_node, heuristic_start)
        graph.set_heuristic(to_node, heuristic_goal)

    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    start_time = time.time()
    
    path, cost, traversal_process = graph.branch_and_bound(start, goal)
    
    end_time = time.time()
    execution_time = end_time - start_time

    if path:
        print(f"Found path: {' -> '.join(path)}")
        print(f"Traversal process: {' -> '.join(traversal_process)}")
        print(f"Total path cost: {cost}")
        print(f"Execution time: {execution_time:.20f} seconds")
    else:
        print("No path found.")

    graph.draw_graph_with_arrows(path)

if __name__ == "__main__":
    main()
