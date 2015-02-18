#!/usr/bin/python

import collections
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
    def contains(self, item):
        return not self.is_empty() and item in zip(*self.elements)[1]
    

def astar(r, c, pacman_r, pacman_c, food_r, food_c, grid):

    # do the search
    result = astar_iterative(r, c, pacman_r, pacman_c, food_r, food_c, grid)

    # print path
    path = reconstruct_path((food_r, food_c), result)
    print len(path)-1  # distance is -1
    for pos in path:
        print str(pos[0]) + ' ' + str(pos[1])


# ---------------------------------------------------------------------------
# A* Search
#
# The A* problem on Hackerrank can actually be solved with a BFS. It only
# checks whether your search finds the optimal solution.
# However this is a full A* nonetheless.
# ---------------------------------------------------------------------------

def astar_iterative(r, c, pacman_r, pacman_c, food_r, food_c, grid):
    fringe = PriorityQueue()  # nodes under consideration
    came_from = {}  # our closed set & node parent information
    cost_so_far = {}  # how expensive has it been to get to this point
    goal = (food_r, food_c)
    start = (pacman_r, pacman_c)

    # start state
    fringe.put(start, 0)
    cost_so_far[start] = 0
    came_from[start] = None

    while not fringe.is_empty() > 0:
        current = fringe.get()

        if is_goal(current, grid):  # done?
            return came_from

        # expand all possible moves from current
        neighbours = get_neighbours(current, grid)
        for next in neighbours:
            
            # cost of move is entire cost so far + cost to move to new node
            new_cost = cost_so_far[current] + cost_of_move(next, grid)

            # don't expand (or explore) nodes twice unless it's cheaper this time
            if (next not in came_from and not fringe.contains(next)) or (new_cost < cost_so_far[next]):
                came_from[next] = current
                cost_so_far[next] = new_cost
                
                # the next node we want to look at is the one with the lowest projected cost
                priority = new_cost + heuristic(next, goal)
                fringe.put(next, new_cost)


# guess how far it is from the point a to point b
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)
                

def cost_of_move(pos, grid):
    return 0 if is_goal(pos, grid) else 1


# gets all neighbours for a position on the grid, only returns valid moves
def get_neighbours(pos, grid):
    (x, y) = pos
    neighbours = [(x-1, y  ),  # up
                  (x,   y-1),  # left
                  (x,   y+1),  # right
                  (x+1, y  )]  # down
    neighbours = filter(lambda x: is_passable(x, grid), neighbours)
    return neighbours


def is_passable(pos, grid):
    return grid[pos[0]][pos[1]] != '%'  # wall


def is_goal(pos, grid):
    return grid[pos[0]][pos[1]] == '.'  # food


def is_start(pos, grid):
    return grid[pos[0]][pos[1]] == 'P'  # pacman


# build path from start to goal
def reconstruct_path(goal, came_from):
    current = goal
    path = [current]
    while not is_start(current, grid):
        current = came_from[current]
        path.append(current)
    return path[::-1]  # reverse




# PREDEFINED TEMPLATE CODE -----------------------------------------
pacman_r, pacman_c = [ int(i) for i in raw_input().strip().split() ]
food_r, food_c = [ int(i) for i in raw_input().strip().split() ]
r,c = [ int(i) for i in raw_input().strip().split() ]

grid = []
for i in xrange(0, r):
    grid.append(raw_input().strip())

astar(r, c, pacman_r, pacman_c, food_r, food_c, grid)
