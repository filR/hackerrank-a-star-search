#!/usr/bin/python

import collections


def dfs(r, c, pacman_r, pacman_c, food_r, food_c, grid):

    # do the search
    result = dfs_iterative(r, c, pacman_r, pacman_c, food_r, food_c, grid)

    # print expanded nodes
    print len(result['visited'])
    for pos in result['visited']:
        print str(pos[0]) + ' ' + str(pos[1])

    # print path
    path = reconstruct_path((food_r, food_c), result['came_from'])
    print len(path)-1  # distance is -1
    for pos in path:
        print str(pos[0]) + ' ' + str(pos[1])


# ---------------------------------------------------------------------------
# Depth First Search
#
# * take element from the fringe
# * if it's the goal -> success
# * otherwise add all of it's neighbours that have not yet been
#     looked at to the fringe
#
# Store the path by recording where we came from.
#   See: http://www.redblobgames.com/pathfinding/a-star/introduction.html
#   Alternative: store not only nodes but also their parents in visited
# ---------------------------------------------------------------------------

def dfs_iterative(r, c, pacman_r, pacman_c, food_r, food_c, grid):
    fringe = collections.deque()  # nodes under consideration
    came_from = {}  # our closed set & node parent information
    visited = []  # only needed for hackerrank - print expanded nodes at end

    # start state
    start = (pacman_r, pacman_c)
    fringe.append(start)
    came_from[start] = None

    while len(fringe) > 0:
        current = fringe.pop()  # depth first
        visited.append(current)

        if is_goal(current, grid):  # done?
            return {'visited': visited, 'came_from': came_from}

        # expand all possible moves from current
        neighbours = get_neighbours(current, grid)
        for next in neighbours:

            # don't expand (or explore) nodes twice
            if next not in came_from and next not in fringe:
                came_from[next] = current
                fringe.append(next)


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

dfs(r, c, pacman_r, pacman_c, food_r, food_c, grid)
