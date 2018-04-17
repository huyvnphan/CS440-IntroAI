# Import Matrix generator module
import numpy
import queue
import math


class Map:
    def __init__(self, size, probability):
        """Initialize a new map object.
        Args:
            size (int): size of map 10 - 1000
            probability (double): 0.0 - 1.0 (0: all empty cells, 1: all walls)
        Returns:
            map object (n*n matrix) with n*n*p empty cells and n*n*(1-p) filled cells
        """
        self.size = size
        self.probability = probability

        # Check if arguments are valid
        if probability > 1 or probability < 0:
            raise ValueError("probability is in range 0 and 1")

        # Generate a uniform distribution matrix (values range from 0.0 to 1.0)
        self.map = numpy.random.uniform(size=[size, size])
        # Generate matrix with n*n*p empty cells
        self.map = (self.map < probability).astype(int)

        # Set start and finish
        self.map[0, 0] = self.map[size - 1, size - 1] = 0

        # Dictionary of solution information
        self.solution = {"Status": "N/A", "Visited cells": [], "No of visited cells": "N/A", "Path": [],
                         "Path length": "N/A"}

    def connected_cells(self, cell):
        """
        Find all connected cells around a cell
        :param cell: list of (x, y) coordinate of a cell in a numpy array
        :return:
        """
        x = cell[0]
        y = cell[1]
        connected_cells = set()
        all_possible_cells = [(x, y + 1), (x - 1, y), (x, y - 1), (x + 1, y)]
        for (i, j) in all_possible_cells:
            if self.in_bounds((i, j)):
                if self.map[i, j] == 0:
                    connected_cells.add((i, j))
        return connected_cells

    def in_bounds(self, cell):
        """
        Check if a cell is in the map
        :param cell: (x, y) coordinate of the cell
        :return: (boolean)
        """
        x = cell[0]
        y = cell[1]
        return (0 <= x < self.size) and (0 <= y < self.size)

    # Print map on console
    def print_map(self):
        print(self.map)

    def print_solution(self):
        print("Status: " + self.solution["Status"])
        print("No of visited cells: " + str(self.solution["No of visited cells"]))
        print("Path length: " + str(self.solution["Path length"]))


class FindSolution:
    def __init__(self, a_map):
        self.a_map = a_map
        self.time = 0
        self.result = "N/A"
        self.start_position = (0, 0)
        self.end_position = (a_map.size - 1, a_map.size - 1)

    def build_path(self, path_dictionary):
        """
        Build a path (list) from a dictionary of parent cell -> child cell
        :param path_dictionary: (dic) (child.x, child,y) -> (parent.x, parent.y) Child:key, Parent:value
        :return: list of path from start to finish
        """
        path = []
        current = path_dictionary[self.end_position]
        while current != (0, 0):
            path += (current,)
            current = path_dictionary[current]
        return path[::-1]

    def dfs(self):
        """
        Find path using Depth First Search
        :return: list of status, visited cell, path, and path length
        """
        a_stack = queue.LifoQueue()
        visited = set()

        a_stack.put(self.start_position)
        visited.add(self.start_position)

        parent_cell = {}

        while not a_stack.empty():
            cell = a_stack.get()
            if cell == self.end_position:
                path = self.build_path(parent_cell)
                return {"Status": "Found Path", "Visited cells": visited,
                        "No of visited cells": len(visited), "Path": path, "Path length": len(path)}

            for child in self.a_map.connected_cells(cell):
                if child not in visited:
                    parent_cell[child] = cell
                    visited.add(child)
                    a_stack.put(child)

        return {"Status": "Path Not Found!!!", "Visited cells": visited,
                "No of visited cells": len(visited), "Path": [], "Path length": "N/A"}

    def bfs(self):
        """
        Find path using Breadth First Search
        :return: list of status, visited cell, path, and path length
        """
        a_queue = queue.Queue()
        visited = set()

        a_queue.put(self.start_position)
        visited.add(self.start_position)

        parent_cell = {}

        while not a_queue.empty():
            cell = a_queue.get()
            if cell == self.end_position:
                path = self.build_path(parent_cell)
                return {"Status": "Found Path", "Visited cells": visited,
                        "No of visited cells": len(visited), "Path": path, "Path length": len(path)}

            for child in self.a_map.connected_cells(cell):
                if child not in visited:
                    parent_cell[child] = cell
                    visited.add(child)
                    a_queue.put(child)

        return {"Status": "Path Not Found!!!", "Visited cells": visited,
                "No of visited cells": len(visited), "Path": [], "Path length": "N/A"}

    def a_star(self, heuristic):
        priority_queue = queue.PriorityQueue()
        visited = set()
        parent_cell = {}
        cost_so_far = {}

        priority_queue.put((0, self.start_position))
        visited.add(self.start_position)
        cost_so_far[self.start_position] = 0

        while not priority_queue.empty():
            current_cell = priority_queue.get()
            current_cell = current_cell[1]
            if current_cell == self.end_position:
                path = self.build_path(parent_cell)
                return {"Status": "Found Path", "Visited cells": visited,
                        "No of visited cells": len(visited), "Path": path, "Path length": len(path)}

            for next_cell in self.a_map.connected_cells(current_cell):
                new_cost = cost_so_far[current_cell] + 1
                if next_cell not in visited:  # or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    parent_cell[next_cell] = current_cell
                    visited.add(next_cell)

                    priority = new_cost + self.find_heuristic(next_cell, heuristic)
                    priority_queue.put((priority, next_cell))

        return {"Status": "Path Not Found!!!", "Visited cells": visited,
                "No of visited cells": len(visited), "Path": [], "Path length": "N/A"}

    def find_heuristic(self, cell, heuristic):
        (x1, y1) = cell
        (x2, y2) = self.end_position
        if heuristic == "euclidean":
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        elif heuristic == "manhattan":
            return abs(x1 - x2) + abs(y1 - y2)
        elif heuristic == "max":
            return max(self.find_heuristic(cell, "euclidean"), self.find_heuristic(cell, "manhattan"))
        elif heuristic == "min":
            return min(self.find_heuristic(cell, "euclidean"), self.find_heuristic(cell, "manhattan"))
        elif heuristic == "alpha":
            alpha = 0.8
            return alpha*self.find_heuristic(cell, "euclidean") + (1-alpha)*self.find_heuristic(cell, "manhattan")
        elif heuristic == "beta":
            beta = 1.8
            return (abs(x1 - x2)**beta + abs(y1 - y2)**beta)**(1/beta)

current_map = Map(2000, 0.2)

print("--------------------------------\nUsing DFS")
current_map.solution = FindSolution(current_map).dfs()
current_map.print_solution()
print("--------------------------------\nUsing BFS")
current_map.solution = FindSolution(current_map).bfs()
current_map.print_solution()
print("--------------------------------\nUsing A* Euclidean")
current_map.solution = FindSolution(current_map).a_star("euclidean")
current_map.print_solution()
print("--------------------------------\nUsing A* Manhattan")
current_map.solution = FindSolution(current_map).a_star("manhattan")
current_map.print_solution()

# Question 8
# print("Using Max Distance")
# p = 0.1
# while p < 0.44:
#     number_of_visited_cells = []
#     for j in range(0, 100):
#         current_map = Map(100, p)
#         current_map.solution = FindSolution(current_map).a_star("max")
#         if type(current_map.solution["No of visited cells"]) == int:
#             number_of_visited_cells.append(current_map.solution["No of visited cells"])
#     print(numpy.mean(number_of_visited_cells))
#     p += 0.05
#
# print("\nUsing Min Distance")
# p = 0.1
# while p < 0.44:
#     number_of_visited_cells = []
#     for j in range(0, 100):
#         current_map = Map(100, p)
#         current_map.solution = FindSolution(current_map).a_star("min")
#         if type(current_map.solution["No of visited cells"]) == int:
#             number_of_visited_cells.append(current_map.solution["No of visited cells"])
#     print(numpy.mean(number_of_visited_cells))
#     p += 0.05

# Question 8
# print("\nUsing Alpha")
# p = 0.1
# while p < 0.44:
#     number_of_visited_cells = []
#     for j in range(0, 100):
#         current_map = Map(100, p)
#         current_map.solution = FindSolution(current_map).a_star("alpha")
#         if type(current_map.solution["No of visited cells"]) == int:
#             number_of_visited_cells.append(current_map.solution["No of visited cells"])
#     print(numpy.mean(number_of_visited_cells))
#     p += 0.05
#
# print("\nUsing Beta")
# p = 0.1
# while p < 0.44:
#     number_of_visited_cells = []
#     for j in range(0, 100):
#         current_map = Map(100, p)
#         current_map.solution = FindSolution(current_map).a_star("alpha")
#         if type(current_map.solution["No of visited cells"]) == int:
#             number_of_visited_cells.append(current_map.solution["No of visited cells"])
#     print(numpy.mean(number_of_visited_cells))
#     p += 0.05