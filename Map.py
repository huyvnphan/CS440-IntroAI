import numpy as np
import heapq as hpq
from itertools import count
TIE = count()

# from sets import Set


class Map():
    def __init__(self, size=10, p=0.1):
        """
        size: number of block per side
        p: prob of wall
        Function create a numpy matrix, 0 denotes traversable
        1 denotes wall
        """

        self.size = size
        if p > 1 or p < 0:
            raise ValueError("p is in range 0 and 1")
        self.map = np.random.uniform(size=[size, size])
        self.map = (self.map < p).astype(int)

        # set start and finish
        self.map[0, 0] = self.map[size - 1, size - 1] = 0

    def print_map(self):
        # for x in self.map:
        #     print x
        print (self.map)

    def isWall(self, index):
        """
        :param index: array of size 2
        :return: bool: if the index is a wall
        """
        return self.map[index]

    def storeMap(self, s):
        with open(s, 'w') as f:
            np.save(f, self.map)

    def loadMap(self, s):
        with open(s, 'r') as f:
            self.map = np.load(f)


def isNeighbor(node1, node2):
    """
    boolean: if 2 nodes are neighbor
    node1, node2: 1d array of 2 elements
    """
    return np.sqrt(((node1 - node2) ** 2).sum()) == 1


class Solution():
    def __init__(self, input_map):
        """
        map: input of type Map
        """
        self.map = input_map
        self.size = self.map.size
        self.MOVE = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        self.goal = np.array([self.size - 1, self.size - 1])
        # self.sol = input_map.map.copy()

    def check_bound(self, indice):
        """
        indice: tuple of coordinate
        """
        if any(j < 0 or j >= self.size for j in indice):
            return False
        elif not self.map.map[indice[0], indice[1]]:
            return True
        else:
            return False

    def DFS(self):
        """
        Depth first search
        """
        sol = self.map.map.copy()
        start = np.array([0, 0])
        stack = []
        stack.append(start)
        # list of sets
        visited = [set() for i in xrange(self.size)]
        path = []
        while stack:
            top = stack.pop()
            path.append(top)
            if np.array_equal(top.flatten(), self.goal.flatten()):
                for i in path:
                    sol[i[0], i[1]] = 2
                return path, sol
            visited[top[0]].add(top[1])
            news = top + self.MOVE
            mask = map(self.check_bound, news)
            temp = []
            for m, child in zip(mask, news):
                # if not out of bound and have not been visited
                if m and child[1] not in visited[child[0]]:
                    temp.append(child)

            if temp:
                stack.extend(temp)
            elif not stack:
                return [], []
            else:
                # backtrack
                path.pop()
                while path and stack and not isNeighbor(path[-1], stack[-1]):
                    path.pop()
                path.append(stack[-1])
                # print stack
        return [], []

    def expand(self, node, visited, queued):
        news = top + self.MOVE
        mask = map(self.check_bound, news)
        temp = []
        for m, child in zip(mask, news):
            # if not out of bound and have not been visited
            if m and child[1] not in visited[child[0]]:
                temp.append(child)
        return temp

    def BFS(self):
        """
        :return: solution and path
        """
        sol = self.map.map.copy().tolist()
        print(sol[0][1])
        start = np.array([0, 0])
        queue = []
        queue.append(start)
        visited = [set() for i in xrange(self.size)]
        queued = [set() for i in xrange(self.size)]
        path = [self.goal]
        debug = self.map.map.copy()
        while queue:
            top = queue.pop(0)
            if np.array_equal(top.flatten(), self.goal.flatten()):
                cur = sol[-1][-1]
                while sol[cur[0]][cur[1]] is not int:
                    path.append(cur)
                    cur = sol[cur[0]][cur[1]]
                    if type(cur) == int:
                        break
                for i in path:
                    debug[i[0], i[1]] = 2
                return path[::-1], debug
            visited[top[0]].add(top[1])
            news = top + self.MOVE
            mask = map(self.check_bound, news)
            temp = []
            for m, child in zip(mask, news):
                if m and child[1] not in visited[child[0]] and child[1] not in queued[child[0]]:
                    temp.append(child)
            if temp:
                queue.extend(temp)
                for t in temp:
                    queued[t[0]].add(t[1])
                    sol[t[0]][t[1]] = top
        return [], []

    def manDist(self, a, b):
        return np.abs(a - b).sum()

    def euclidean(self, a, b):
        return np.sqrt(((a - b) ** 2).sum())

    def As_manhattan(self, heuristic='man'):
        """
        :return: solution and path
        """
        heu = None
        if heuristic == 'man':
            heu = self.manDist
        elif heuristic == 'eu':
            heu = self.euclidean
        sol = self.map.map.copy().tolist()
        print(sol[0][1])
        start = np.array([0, 0])
        queue = []
        hpq.heappush(queue, (0, next(TIE), start))
        visited = [set() for i in xrange(self.size)]
        queued = [set() for i in xrange(self.size)]
        path = [self.goal]
        debug = self.map.map.copy()
        while queue:
            top = hpq.heappop(queue)[2]
            # print top
            if np.array_equal(top.flatten(), self.goal.flatten()):
                cur = sol[-1][-1]
                while sol[cur[0]][cur[1]] is not int:
                    path.append(cur)
                    cur = sol[cur[0]][cur[1]]
                    if type(cur) == int:
                        break
                for i in path:
                    debug[i[0], i[1]] = 2
                return path[::-1], debug
            visited[top[0]].add(top[1])
            news = top + self.MOVE
            mask = map(self.check_bound, news)
            temp = []
            for m, child in zip(mask, news):
                if m and child[1] not in visited[child[0]] and child[1] not in queued[child[0]]:
                    temp.append(child)
            if temp:
                # queue.extend(temp)
                for t in temp:
                    d = heu(np.array([0, 0]), t)
                    # print d, t
                    hpq.heappush(queue, (d, next(TIE), t))
                    queued[t[0]].add(t[1])
                    sol[t[0]][t[1]] = top
        return [], []


myMap = Map(size=10, p=.3)
# myMap.storeMap('temp.npz')
myMap.loadMap('temp.npz')
myMap.print_map()

mySol = Solution(myMap)
# print (mySol.check_bound((1,7)))
# print(isNeighbor(np.array([6, 7]), np.array([5, 7])))
path, sol = mySol.DFS()
print (sol)
print (list(path))
print (len(path))
path, sol = mySol.BFS()
print (sol)
print (path)
print (len(path))
path, sol = mySol.As_manhattan()
print (sol)
print (path)
print (len(path))
path, sol = mySol.As_manhattan(heuristic='eu')
print (sol)
print (path)
print (len(path))