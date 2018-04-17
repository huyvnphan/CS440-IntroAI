import numpy as np
import random

SIZE = 5

class MazeSearch:
    def __init__(self):
        self.maze = np.zeros((SIZE, SIZE), dtype=np.float64)
        for i in range(0, SIZE):
            for j in range(0, SIZE):
                self.maze[i,j] = random.choice([0.2, 0.4, 0.6, 0.9])

        self.probability_containing = np.full((SIZE, SIZE), 1/(SIZE*SIZE), dtype=np.float64)
        self.probability_finding = self.probability_containing

    def print(self):
        print("Maze\n")
        print(self.maze)
        print("\n\nProbability containing target\n")
        print(self.probability_finding)
        print("\n\nProbability finding target\n" + self.probability_finding + "\n\n")

myMaze = MazeSearch()
myMaze.print()