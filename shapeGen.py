from graphics import *

################################################################################
# Code for fixed obstacle generation
################################################################################

# Returns a list of hard-coded targets
def setTargets(win):
    targets = []
    #declare targets here
    targets = addTarget(win, targets, 600, 350, 30)
    targets = addTarget(win, targets, 800, 200, 30)
    return targets


# Returns a list of hard-coded obstacles
def setObstacles(win):
    obstacles = []
    #declare obstacles here
    obstacles = addGradedWall(win, obstacles, [100, 150, 750, 400], 1)
    obstacles = addGradedWall(win, obstacles, [300, 400, 550, 400], 2)
    obstacles = addGradedWall(win, obstacles, [500, 400, 750, 350], 3)
    obstacles = addGradedWall(win, obstacles, [500, 100, 1000, 1030], 3)
    return obstacles


# Creates and draws a new target (a green circle)
def addTarget(win, targets, x, y, size):
    target = Circle(Point(x, y), size)
    target.setFill("#68ED44")
    target.draw(win)
    targets.append(target)
    return targets


# Creates and draws a new obstacle, colour coded based on strength
def addGradedWall(win, obstacles, obstacleDimensions, grade):
    y1, y2, x1, x2 = obstacleDimensions
    wallColours = ["#CCCCCC", "#999999", "#666666"]
    for i in range (grade):
        wall = Rectangle(Point(x1, y1), Point(x2, y2))
        wall.setFill(wallColours[i])
        wall.draw(win)
        obstacles.append(wall)
    return obstacles