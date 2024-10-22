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
        heap = [(self.heuristic[start], start, [start])]  # (cost + heuristic, node, path)
        visited = set()
        traversal_process = []  # Store traversal process

        while heap:
            current_cost, current_node, path = heapq.heappop(heap)

            if current_node in visited:
                continue

            visited.add(current_node)
            traversal_process.append(current_node)  # Add current node to traversal process

            if current_node == goal:
                return path, current_cost, traversal_process

            for neighbor, cost in self.graph.get(current_node, []):
                if neighbor not in visited:
                    new_cost = current_cost - self.heuristic[current_node] + cost + self.heuristic[neighbor]
                    heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

        return None, float('inf'), traversal_process

    def draw_graph(self, path, traversal_process):
        G = nx.DiGraph()

        # Add edges from the graph with weights
        for from_node in self.graph:
            for to_node, cost in self.graph[from_node]:
                G.add_edge(from_node, to_node, weight=cost)

        pos = nx.spring_layout(G)

        # Draw the graph
        plt.figure(figsize=(10, 7))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')

        # Draw edge labels
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Highlight the traversal process and path
        if traversal_process:
            nx.draw_networkx_nodes(G, pos, nodelist=traversal_process, node_color='yellow', node_size=3000)
        
        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        plt.title("Branch and Bound Traversal and Path")
        plt.show()

def main():
    graph = Graph()

    # Read data from file
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # Process each line of data
    for line in lines:
        from_node, to_node, cost, heuristic_start, heuristic_goal = line.split()
        cost = float(cost)
        heuristic_start = float(heuristic_start)
        heuristic_goal = float(heuristic_goal)
        
        graph.add_edge(from_node, to_node, cost)
        graph.set_heuristic(from_node, heuristic_start)
        graph.set_heuristic(to_node, heuristic_goal)

    # Enter start and goal nodes from the user
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    # Measure the algorithm execution time
    start_time = time.time()
    
    # Run the Branch and Bound algorithm
    path, cost, traversal_process = graph.branch_and_bound(start, goal)
    
    end_time = time.time()
    execution_time = end_time - start_time

    # Output the results
    if path:
        print(f"Found path: {' -> '.join(path)}")
        print(f"Traversal process: {' -> '.join(traversal_process)}")
        print(f"Total path cost: {cost}")
        print(f"Execution time: {execution_time:.20f} seconds")
    else:
        print("No path found.")

    # Draw the graph and highlight the path
    graph.draw_graph(path, traversal_process)

if __name__ == "__main__":
    main()
