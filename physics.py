from graphics import *
from datetime import datetime
import math


# Simulates projectile motion based on the given parameters using SUVAT
def simulateProjectile(win, start, clickPos, obstacles, targets, physicsConstants):

    # Load constants
    fps, forceMetric, friction, elasticity, gravity = physicsConstants
    tickLength = 1/fps
    timeMetric = 0.01 # Hidden constant for calibrating simulation speed
    g = gravity * timeMetric
    fm = forceMetric * timeMetric

    # Draw cross-hair
    crosshair = Text(clickPos, "X")
    crosshair.setSize(10)
    crosshair.setTextColor("blue")
    crosshair.draw(win)

    # Start position
    x = start.getX()
    y = start.getY()

    # Start velocity
    Ux = (horizontalDistance(start, clickPos) * fm)
    Uy = (verticalDistance(start, clickPos) * fm)
    #If released above catapult, shoot downwards
    if clickPos.getY() < start.getY():
        Uy = Uy * -1

    t = 0 # Unit time (Number of ticks since arc started)
    canBreak = True # Determines projectiles ability to damage/destroy obstacles
    stationary = False # Ensure run once
    projectile = drawProjectile(win, start) # Draw projectile

    while not outOfBounds(win,x,y):

        # Time for game speed
        startTime = datetime.now()

        newPoint = Point(x, y)

        # Run SUVAT
        Sx = Ux * t
        Sy = Uy * t + 0.5 * -g * t ** 2
        y = start.getY() - Sy
        x = start.getX() + Sx
        t = t + 1

        collided = checkForCollisions(x, y, obstacles, targets)
        if collided != None:
            # Determine nature of collision

            # Impacted from the side
            impactCheck = checkCollision(newPoint.getX(), y, collided)
            if not impactCheck:
                Ux = Ux * elasticity * -1   # Bounce
            else:
                Ux = Ux * (1-friction)      # Apply friction

            # Impacted from above/below
            impactCheck = checkCollision(x, newPoint.getY(), collided)
            if not impactCheck:
                Uy = (Uy + -g * t) * elasticity * -1 # Bounce
            else:
                Uy = (Uy + -g * t) * (1-friction)    # Apply friction

            # Interact with object hit
            if type(collided) == Circle: # If target then destroy
                collided.undraw()
                targets.remove(collided)
            elif canBreak:           # Otherwise try to damage obstacle
                collided.undraw()
                obstacles.remove(collided)

            # End simulation if no movement
            if stationary:
                time.sleep(0.5) # Prevent instant disappearance
                projectile.undraw()
                break
            if Ux ** 2 < 1 and Uy ** 2 < 1: # Ensures reasonable tolerance of minor movement
                stationary = True
            else:
                stationary = False

            # Prepare for new arc
            t = 1
            start = newPoint
            canBreak = False # Can only break on first collision

        # => movement step complete
        projectile.undraw()
        projectile = drawProjectile(win, newPoint)

        # Time for game speed
        duration = datetime.now() - startTime
        elapsedTime = duration.total_seconds()
        print(elapsedTime)
        if elapsedTime < tickLength:
            sleepTime = tickLength - elapsedTime
            time.sleep(sleepTime) # Wait before next step

    # => Projectile out of bounds (off-screen)
    projectile.undraw()


# Whether the point x,y is out of bounds
def outOfBounds(win,x,y):
    return x >= win.getWidth() or x <= 0 or y >= win.getHeight();


# Draws a projectile at position or otherwise a position indicator if out of bounds
def drawProjectile(win, position):

    # If projectile is above top of window, display indicator instead
    if position.getY() < 0:
        bottom = Point(position.getX(), 10)
        top = Point(position.getX(), 2)
        projectile = Line(bottom, top)
        projectile.setArrow('last')
    else:
        projectile = Circle(position, 5)

    projectile.setFill("blue")
    projectile.draw(win)
    return projectile


# Checks if a point collides with any obstacle or target
def checkForCollisions(x, y, obstacles, targets):
    for i in range(len(targets)):
        if checkCollision(x, y, targets[i]):
            return targets[i]
    for i in range(len(obstacles)-1, -1, -1):
        if checkCollision(x, y, obstacles[i]):
            return obstacles[i]
    return None


# Checks if a point collides with a shape (circle or rectangle)
def checkCollision(x, y, target):
    if type(target) == Circle:
        # Point in circle
        if distance(Point(x, y), target.getCenter()) <= target.getRadius():
            return True
    else:
        # Point in rectangle
        top, bottom, left, right = determineRectangleBounds(target)
        if x >= left and x <= right and y >= top and y <= bottom:
            return True
    return False


# Calculates the bounds of a rectangle
def determineRectangleBounds(rectangle):
    p1 = rectangle.getP1()
    p2 = rectangle.getP2()
    if p1.getX() < p2.getX():
        left = p1.getX()
        right = p2.getX()
    else:
        left = p2.getX()
        right = p1.getX()
    if p1.getY() < p2.getY():
        top = p1.getY()
        bottom = p2.getY()
    else:
        top = p2.getY()
        bottom = p1.getY()
    return top, bottom, left, right


# Calculates the distance between two points
def distance(p1, p2):
    # Pythagoras theorem
    return(math.sqrt(((p2.getX() - p1.getX()) ** 2) \
           + ((p2.getY() - p1.getY()) ** 2)))


# Calculates the absolute horizontal distance between two points
def horizontalDistance(p1, p2):
    return abs(p2.getX() - p1.getX())


# Calculates the absolute vertical distance between two points
def verticalDistance(p1, p2):
    return abs((p2.getY() - p1.getY()))