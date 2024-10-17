import heapq

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

    # Đọc dữ liệu từ file
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    # Xử lý từng dòng dữ liệu
    for line in lines:
        from_node, to_node, cost, heuristic_start, heuristic_goal = line.split()
        cost = float(cost)
        heuristic_start = float(heuristic_start)
        heuristic_goal = float(heuristic_goal)
        
        graph.add_edge(from_node, to_node, cost)
        graph.set_heuristic(from_node, heuristic_start)
        graph.set_heuristic(to_node, heuristic_goal)

    # Nhập đỉnh bắt đầu và đỉnh đích từ người dùng
    start = input("Nhập đỉnh bắt đầu: ")
    goal = input("Nhập đỉnh đích: ")

    # Chạy thuật toán Branch and Bound
    path, cost = graph.branch_and_bound(start, goal)

    if path:
        print(f"Đường đi tìm được: {' -> '.join(path)} với tổng chi phí: {cost}")
    else:
        print("Không tìm được đường đi.")

if __name__ == "__main__":
    main()
