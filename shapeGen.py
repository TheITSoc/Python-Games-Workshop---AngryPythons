from graphics import *
import physics
import random



################################################################################
# Code for fixed obstacle generation
################################################################################

# Returns a list of hard-coded targets
def setTargets(win):
    targets = []
    #declare targets here
    targets = addTarget(win, targets, 600, 450, 30)
    targets = addTarget(win, targets, 800, 200, 30)
    return targets


# Returns a list of hard-coded obstacles
def setObstacles(win):
    obstacles = []
    #declare obstacles here
    obstacles = addGradedWall(win, obstacles, [700, 500, 750, 400], 1)
    obstacles = addGradedWall(win, obstacles, [500, 500, 550, 400], 2)
    obstacles = addGradedWall(win, obstacles, [500, 400, 750, 350], 3)
    return obstacles


# Creates and draws a new target (a green circle)
def addTarget(win, targets, x, y, size):
    target = Circle(Point(x, y), size)
    target.setFill("green")
    target.draw(win)
    targets.append(target)
    return targets


# Creates and draws a new obstacle, colour coded based on strength
def addGradedWall(win, obstacles, obstacleDimensions, grade):
    y1, y2, x1, x2 = obstacleDimensions
    wallColours = ["brown", "grey", "gold"]
    for i in range (grade):
        wall = Rectangle(Point(x1, y1), Point(x2, y2))
        wall.setFill(wallColours[i])
        wall.draw(win)
        obstacles.append(wall)
    return obstacles




################################################################################
# Code for random obstacle generation
################################################################################

# Procedurally generates a list of non-overlapping targets
def genRandomTargets(win, targetNumber, obstacles):
    targets = []
    startTime = time.clock() # For timeout
    for i in range(targetNumber):
        # Prevent overlap
        collided = True # Ensure run once
        while collided == True:
            # Generate random size and position
            size = random.randint(20, 40)
            x = random.randint(win.getWidth() // 5 + size, win.getWidth() - size)
            y = random.randint(size, win.getHeight()-size)

            # Calculate bounding box
            top = y - size
            bottom = y + size
            left = x - size
            right = x + size
            obstacleDimensions = top, bottom, left, right

            #  Test for overlap
            if circleOverlapsObstacle(Point(x, y), size, obstacles) \
            or circleOverlapsTarget(Point(x, y), size, targets) \
            or checkForObstacleOverlap(obstacleDimensions, obstacles):
                collided = True
                if time.clock() - startTime >= 30: #timeout
                    return []
            else:
                collided = False

        # => Successfully generated valid target parameters
        targets = addTarget(win, targets, x, y, size)

    # => Generated desired number of targets successfully
    return targets


# Procedurally generates a list of non-overlapping obstacles
def genRandomObstacles(win, obstacleNumber, obstacleDimensionRanges):
    obstacles = []
    startTime = time.clock() # For timeout
    for i in range(obstacleNumber):
        collided = True # Ensure run once
        while collided == True:
            # Randomly pick rotation
            longSide = random.randint(0, 1)

            # Generate random dimensions
            obstacleDimensions = \
            genTallOrWideRectangle(win, obstacleDimensionRanges, longSide)

            # Test for overlap
            if rectanglePointsInsideObstacle(obstacleDimensions, obstacles) \
            or checkForObstacleOverlap(obstacleDimensions, obstacles):
                collided = True
                if time.clock() - startTime >= 30: #timeout
                    return []
            else:
                collided = False

        # => Successfully generated valid obstacle position & dimensions
        grade = random.randint(1, 3) # Randomly pick obstacle strength
        obstacles = addGradedWall(win, obstacles, obstacleDimensions, grade)

    # => Generated desired number of obstacles successfully
    return obstacles


# Generates a rectangle with random dimensions (within obstacleDimensionRanges)
def genTallOrWideRectangle(win, obstacleDimensionRanges, longSide):
    shortMin, shortMax, longMin, longMax = obstacleDimensionRanges

    # Generate random side lengths
    long = random.randint(longMin, longMax)
    short = random.randint(shortMin, shortMax)

    # Assign long-side & calculate rectangle edges
    if longSide == 0:
        left = random.randint(win.getWidth() // 5, win.getWidth() - long)
        right = left + long
        top = random.randint(0, win.getHeight() - short)
        bottom = top + short
    else:
        left = random.randint(win.getWidth() // 5, win.getWidth() - short)
        right = left + short
        top = random.randint(0, win.getHeight() - long)
        bottom = top + long
    #rectangle = Rectangle(Point(left,top),Point(right,bottom))
    return top, bottom, left, right


# Checks is the bounding points of a rectangle overlap any of a list
# of other rectangles
def rectanglePointsInsideObstacle(obstacleDimensions, obstacles):
    top, bottom, left, right = obstacleDimensions
    if physics.checkForCollisions(left, top, obstacles, []) != None \
    or physics.checkForCollisions(left, bottom, obstacles, []) != None \
    or physics.checkForCollisions(right, top, obstacles, []) != None \
    or physics.checkForCollisions(right, bottom, obstacles, []):
        return True
    return False


# Checks if a circle overlaps any of a list of rectangles
def circleOverlapsObstacle(center, radius, obstacles):
    for obstacle in obstacles:
        top, bottom, left, right = physics.determineRectangleBounds(obstacle)
        if isBetween(center.getX(), left-radius, right + radius)\
        and isBetween(center.getY(), top-radius, bottom + radius):
            return True
    return False


# Checks if a circle overlaps any of a list of other circles
def circleOverlapsTarget(center, radius, targets):
    for target in targets:
        if physics.distance(center, target.getCenter()) <= radius + target.getRadius():
            return True
    return False


# Checks if one obstacle would overlap any other
def checkForObstacleOverlap(obstacleDimensions, obstacles):
    newTop, newBottom, newLeft, newRight = obstacleDimensions
    for obstacle in obstacles:
        obTop, obBottom, obLeft, obRight = physics.determineRectangleBounds(obstacle)
        if isBetween(newTop, obTop, obBottom) \
        or isBetween(newBottom, obTop, obBottom):
            if newLeft < obLeft and newRight > obRight:
                return True
        if isBetween(newLeft, obLeft, obRight) \
        or isBetween(newRight, obLeft, obRight):
            if newTop < obTop and newBottom > obBottom:
                return True
    return False


# Determines if a value is within a range
def isBetween(queryValue, bound1, bound2):
    if queryValue >= bound1 and queryValue <= bound2 \
    or queryValue >= bound2 and queryValue <= bound1:
        return True
    return False