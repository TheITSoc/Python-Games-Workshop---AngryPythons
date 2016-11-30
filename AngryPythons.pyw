from graphics import *
import physics
import shapeGen


# Program entry point, opens window and displays options menu
def main(width, height):
    win = GraphWin("PyBirds", width, height)
    # Keep running the game until the window is closed
    while True:
        play(win)


# Run the game
def play(win):

    # Load options
    ammo = 5
    physicsConstants = (90, 10, 0.15, 0.5, 9.8)

    # Coordinate of top of catapult
    topOfCatapult = Point(win.getWidth() / 10, win.getHeight() * 4 / 5)

    # Draw constants and UI
    drawBackdrop(win)
    drawScenery(win, topOfCatapult)
    ammoDisplay = Text(Point(10, 10), ammo)
    ammoDisplay.draw(win)

    # Generate level
    obstacles = shapeGen.setObstacles(win)
    targets = shapeGen.setTargets(win)

    won = False
    lost = False

    # Game loop
    while not won and not lost:

        # Listen for user interaction
        clickPos = getUserInput(win)

        # Update ammo
        ammo = ammo - 1
        ammoDisplay.setText(ammo)

        drawCrosshair(win,clickPos)
        physics.simulateProjectile(win, topOfCatapult, clickPos, obstacles, targets, physicsConstants)

        # win when no targets are left
        won = len(targets) == 0
        # lose when ammo runs out
        lost = ammo == 0

    if won:
        showMessage(win, "You win", "darkgreen", "yellow")
    elif lost:
        showMessage(win, "Out of ammo", "red", "orange")

    # Clean up these objects, then return
    undrawAll(targets)
    undrawAll(obstacles)
    return


# Wait for the user to click in a valid firing position
def getUserInput(win):
    clickPos = win.getMouse()
    # Ignore clicks that are out of bounds (right of catapult)
    while clickPos.getX() > win.getWidth() / 10:
        clickPos = win.getMouse()
    return clickPos


def undrawAll(shapes):
    for shape in shapes:
        shape.undraw()



################################################################################
# Code for drawing
################################################################################

# Drawns an X at Point pos
def drawCrosshair(win, pos):
    crosshair = Text(pos, "X")
    crosshair.setSize(10)
    crosshair.setTextColor("blue")
    crosshair.draw(win)


# Displays message in the middle of the screen with a coloured backdrop
def showMessage(win, message, textColour, bgColour):

    # Position
    center = Point(win.getWidth() / 2, win.getHeight() / 2)
    topLeft = Point(center.getX()-150, center.getY()-40)
    bottomRight = Point(center.getX() + 150, center.getY() + 40)

    bg = Rectangle (topLeft, bottomRight)
    txt = Text(center, message)

    # Set display properties
    txt.setSize(20)
    bg.setFill(bgColour)
    txt.setFill(textColour)

    # Display and wait till clicked
    bg.draw(win)
    txt.draw(win)
    win.getMouse()


# Fills the screen with a solid colour
def drawBackdrop(win):
    topLeft = Point(0, 0)
    bottomRight = Point(win.getWidth(), win.getHeight())
    backdrop = Rectangle(topLeft, bottomRight)
    backdrop.setFill("#D3D3D3")
    backdrop.draw(win)


# Draws the game's static scenary
def drawScenery(win, topOfCatapult):
    # Draw power rings
    outerRingRadius = win.getWidth() / 8
    # Draw a red ring at full size
    redRing = Circle(topOfCatapult, outerRingRadius)
    redRing.setFill("red")
    redRing.draw(win)
    # Draw a yellow ring on top, 2/3 the size of the red ring
    yellowRing = Circle(topOfCatapult, outerRingRadius * 2 / 3)
    yellowRing.setFill("yellow")
    yellowRing.draw(win)
    # Draw a green ring on top, 1/3 the size of the red ring
    greenRing = Circle(topOfCatapult, outerRingRadius / 3)
    greenRing.setFill("green")
    greenRing.draw(win)

    # Draw catapult
    catapultBottomPos = Point(topOfCatapult.getX() - 5, win.getHeight())
    catapult = Rectangle(topOfCatapult, catapultBottomPos)
    catapult.setFill("brown")
    catapult.draw(win)

    # Draw the sky
    skyTopLeft = Point(win.getWidth() / 10, 0)
    skyBottomRight = Point(win.getWidth(), win.getHeight() + 10)
    sky = Rectangle(skyTopLeft, skyBottomRight)
    sky.setFill("lightblue")
    sky.draw(win)



main(1200, 500)
