#!/usr/bin/python
def dfs (r, c, pacman_r, pacman_c, food_r, food_c, grid):
    result = dfs_iterative (r, c, pacman_r, pacman_c, food_r, food_c, grid)
    
    # print expanded nodes
    print len(result['visited'])
    for pos in result['visited']:
        print str(pos[0]) + ' ' + str(pos[1])
        
    # print path
    path = reconstructPath((food_r, food_c), result['came_from'])
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

def dfs_iterative (r, c, pacman_r, pacman_c, food_r, food_c, grid):
    fringe = []  # list of nodes under consideration
    visited = []  # list of nodes already expanded
    came_from = [[0 for x in range(c)] for x in range(r)]  # store information on how to get to the goal
    
    # start state
    fringe.append((pacman_r, pacman_c))
    
    while len(fringe) > 0:
        current = fringe.pop()  # depth first
        visited.append(current)
        
        if isGoal(current, grid):  # done?
            return { 'visited': visited, 'came_from': came_from }
        
        # expand all possible moves from current
        neighbours = getNeighbours(current, grid)
        neighbours = purgeAlreadyExpanded(neighbours, visited, fringe)
        storeCameFrom(neighbours, current, came_from)
        fringe += neighbours
        

# store information about our path
def storeCameFrom (nodes, parent, map):
    for node in nodes:
        map[node[0]][node[1]] = parent

# filters our the nodes we have already expanded and/or explored
def purgeAlreadyExpanded (nodes, visited, fringe):
    nodes = filter(lambda el: el not in visited, nodes)
    nodes = filter(lambda el: el not in fringe, nodes)
    return nodes
        
# gets all neighbours for a position on the grid, only returns valid moves
def getNeighbours (pos, grid):
    neighbours = []
    neighbours.append(checkValidMove((pos[0]-1, pos[1]),   grid))  # up
    neighbours.append(checkValidMove((pos[0],   pos[1]-1), grid))  # right
    neighbours.append(checkValidMove((pos[0],   pos[1]+1), grid))  # left
    neighbours.append(checkValidMove((pos[0]+1, pos[1]),   grid))  # down
    neighbours = filter(None, neighbours)  # filter illegal moves
    return neighbours

# make sure move is valid
def checkValidMove (pos, grid):
    if grid[pos[0]][pos[1]] != '%':  # wall
        return pos

def isGoal (pos, grid):
    return grid[pos[0]][pos[1]] == '.'  # food

def isStart (pos, grid):
    return grid[pos[0]][pos[1]] == 'P'  # pacman

# build the path from the goal back to the start, using our records
def reconstructPath (goal, came_from):
    path = [goal]
    while not isStart(path[-1], grid):
        current = (path[-1][0], path[-1][1])
        next = came_from[current[0]][current[1]]
        path.append(next)
    return path[::-1]  # reverse




# PREDEFINED TEMPLATE CODE BELOW -----------------------------------
pacman_r, pacman_c = [ int(i) for i in raw_input().strip().split() ]
food_r, food_c = [ int(i) for i in raw_input().strip().split() ]
r,c = [ int(i) for i in raw_input().strip().split() ]

grid = []
for i in xrange(0, r):
    grid.append(raw_input().strip())

dfs(r, c, pacman_r, pacman_c, food_r, food_c, grid)
