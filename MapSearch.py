# Import the GUI Module.
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Import Matrix generator module
import numpy
import queue
import math

FRAME_WIDTH = 700
DEFAULT_SIZE = 100
DEFAULT_PROBABILITY = 0.2
COLOR_LIST = [["#F44336", "#FFCDD2"], ["#2196F3", "#BBDEFB"], ["#4CAF50", "#C8E6C9"],
              ["#FF9800", "#FFE0B2"], ["#E91E63", "#F8BBD0"], ["#9C27B0", "#E1BEE7"]]
color = []


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

    # Draw map on canvas
    def draw_map(self, canvas):
        # Determine the width of each cell
        width = FRAME_WIDTH / self.size
        for x in range(0, self.size):
            for y in range(0, self.size):
                points = [(x * width, y * width), ((x + 1) * width, y * width),
                          ((x + 1) * width, (y + 1) * width), ((x * width), (y + 1) * width)]

                # Draw first and last cell
                if (x, y) == (0, 0) or (x, y) == (self.size - 1, self.size - 1):
                    canvas.draw_polygon(points, 1, "Black", "#00FF00")
                # Draw path from start to finish
                elif (x, y) in self.solution["Path"]:
                    canvas.draw_polygon(points, 1, "Black", color[0])
                # Draw visited cells
                elif (x, y) in self.solution["Visited cells"] and (x, y) not in self.solution["Path"]:
                    canvas.draw_polygon(points, 1, "Black", color[1])
                # Draw empty cells
                elif self.map[x, y] == 0:
                    canvas.draw_polygon(points, 1, "Black", "White")
                # Draw walls
                else:
                    canvas.draw_polygon(points, 1, "Black", "#464646")


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
            current_cell = a_stack.get()
            if current_cell == self.end_position:
                path = self.build_path(parent_cell)
                return {"Status": "Found Path", "Visited cells": visited,
                        "No of visited cells": len(visited), "Path": path, "Path length": len(path)}

            for next_cell in self.a_map.connected_cells(current_cell):
                if next_cell not in visited:
                    parent_cell[next_cell] = current_cell
                    visited.add(next_cell)
                    a_stack.put(next_cell)

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
            current_cell = a_queue.get()
            if current_cell == self.end_position:
                path = self.build_path(parent_cell)
                return {"Status": "Found Path", "Visited cells": visited,
                        "No of visited cells": len(visited), "Path": path, "Path length": len(path)}

            for next_cell in self.a_map.connected_cells(current_cell):
                if next_cell not in visited:
                    parent_cell[next_cell] = current_cell
                    visited.add(next_cell)
                    a_queue.put(next_cell)

        return {"Status": "Path Not Found!!!", "Visited cells": visited,
                "No of visited cells": len(visited), "Path": [], "Path length": "N/A"}

    def a_star(self, heuristic):
        """
        Find path using A*
        :param heuristic: "euclidean" or "manhattan"
        :return: list of status, visited cell, path, and path length
        """
        priority_queue = queue.PriorityQueue()
        visited = set()
        parent_cell = {}
        cost_so_far = {}  # Cost from start to each cell

        # Put in que as tuple (priority, cell)
        priority_queue.put((0, self.start_position))
        visited.add(self.start_position)
        cost_so_far[self.start_position] = 0

        while not priority_queue.empty():
            current_cell = priority_queue.get()
            # Get the cell only, don't care about priority
            current_cell = current_cell[1]
            if current_cell == self.end_position:
                path = self.build_path(parent_cell)
                return {"Status": "Found Path", "Visited cells": visited,
                        "No of visited cells": len(visited), "Path": path, "Path length": len(path)}

            for next_cell in self.a_map.connected_cells(current_cell):
                new_cost = cost_so_far[current_cell] + 1
                if next_cell not in visited:
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


def generate_map():
    global current_map
    current_map = Map(int(input_size.get_text()), float(input_probability.get_text()))
    update()


def draw_handler(canvas):
    current_map.draw_map(canvas)


def input_handler():
    pass


def solve_with_dfs():
    global current_map, color
    color = COLOR_LIST[0]
    current_map.solution = FindSolution(current_map).dfs()
    algorithm_used.set_text("Algorithm used: DFS")
    update()


def solve_with_bfs():
    global current_map, color
    color = COLOR_LIST[1]
    current_map.solution = FindSolution(current_map).bfs()
    algorithm_used.set_text("Algorithm used: BFS")
    update()


def solve_with_a_star_euclidean():
    global current_map, color
    color = COLOR_LIST[2]
    current_map.solution = FindSolution(current_map).a_star("euclidean")
    algorithm_used.set_text("Algorithm used: A* Euclidean")

    update()


def solve_with_a_star_manhattan():
    global current_map, color
    color = COLOR_LIST[3]
    current_map.solution = FindSolution(current_map).a_star("manhattan")
    algorithm_used.set_text("Algorithm used: A* Manhattan")
    update()


def update():
    status_label.set_text("STATUS: " + current_map.solution["Status"])
    path_length_label.set_text("PATH LENGTH: " + str(current_map.solution["Path length"]))
    no_of_visited_cells_label.set_text("NO OF VISITED CELLS: " + str(current_map.solution["No of visited cells"]))


current_map = Map(DEFAULT_SIZE, DEFAULT_PROBABILITY)

# Create frame and control UI
frame = simplegui.create_frame('Assignment 1', FRAME_WIDTH, FRAME_WIDTH)
frame.add_button("Generate Map", generate_map, 100)
frame.set_draw_handler(draw_handler)
input_size = frame.add_input('Size', input_handler, 50)
input_size.set_text(str(DEFAULT_SIZE))
input_probability = frame.add_input("Probability", input_handler, 50)
input_probability.set_text(str(DEFAULT_PROBABILITY))

# Algorithms
frame.add_label("")
frame.add_label("Algorithm")
frame.add_button("DFS", solve_with_dfs, 100)
frame.add_button("BFS", solve_with_bfs, 100)
frame.add_button("A* Euclidean", solve_with_a_star_euclidean, 100)
frame.add_button("A* Manhattan", solve_with_a_star_manhattan, 100)

# Display status
frame.add_label("")
algorithm_used = frame.add_label("Algorithm used: N/A")
status_label = frame.add_label("STATUS: N/A")
no_of_visited_cells_label = frame.add_label("NO OF VISITED CELLS: N/A")
path_length_label = frame.add_label("PATH LENGTH: N/A")

frame.start()
