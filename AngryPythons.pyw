from graphics import *
import physics
import shapeGen

# Below are some constants that are globabaly visible to make the code simpler
# Note that in Python, a tuple is a list that cannot be modified

# Tuple of the description text for each menu option
MENU_STRINGS = (
                "Number of targets",
                "Number of obstacles",
                "Ammo",
                "Ticks per second",
                "Force multiplier",
                "Surface friction",
                "Projectile elasticity",
                "Gravity",
                "Min obstacle width",
                "Max obstacle width",
                "Min obstacle length",
                "Max obstacle length")

# Tuple of default values for each menu option
MENU_DEFAULTS = (
                 "3", "10", "10",
                 "90", "10", "0.15", "0.5", "9.8",
                 "10", "30", "70", "300")

# Number of columns in the menu (must be even)
MENU_COLUMN_NUMBER = 4



# Program entry point, opens window and displays options menu
def main(width, height):

    win = GraphWin("PyBirds", width, height)
    menuInputs = intialiseMenuInputs()
    while True:
        menuInputs = menu(win, menuInputs)


# Run the game with the specified options
def play(win, options):

    # Load options from menu
    targetNumber = options[0]
    obstacleNumber = options[1]
    ammo = options[2]
    physicsConstants = options[3:8]
    obstacleDimensionRanges = options[8:12]

    # Coordinate of top of catapult
    topOfCatapult = Point(win.getWidth() / 10, win.getHeight() * 4 / 5)

    # Draw constants and UI
    drawBackdrop(win)
    drawScenery(win, topOfCatapult)
    menuButton = drawButton(win, [0, 20, 0, 80], "red", "Menu", "gold")
    ammoDisplay = Text(Point(100, 10), ammo)
    ammoDisplay.draw(win)

    # Generate level
    obstacles = shapeGen.genRandomObstacles(win, obstacleNumber, obstacleDimensionRanges)
    targets = shapeGen.genRandomTargets(win, targetNumber, obstacles)
    # Uncomment below for hard-coded level layout
    #obstacles = shapeGen.setObstacles(win)
    #targets = shapeGen.setTargets(win)

    won = False
    lost = False

    # Game loop
    while not won and not lost:

        # Listen for user interaction
        clickPos = getUserInput(win)

        # Check if user clicked the menu button
        if mouseOverrectangle(clickPos, menuButton):
            return # End game and return to menu

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

    # Clean up these objects, then return to the menu
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
# Code for Options Menu
################################################################################

# Draws the options menu
def menu(win, menuInputs):

    # Draw the background (i.e. clear the screen)
    drawBackdrop(win)

    # Create and draw the Play and Defaults buttons
    playButton = drawButton(win, [0, 20, 0, 80], "darkgreen", "Play", "gold")
    defaultsButton = drawButton(win, [0, 20, 80, 160], "gold", "Defaults", "red")

    # Draw all the menu options input fields
    for item in menuInputs:
        item.draw(win)

    # Draw the labels for each menu option
    drawMenuItemLabels(win)

    # Listen for click of Play or Defaults button by checking the mouse position
    # each time the user clicks until it's within one of the buttons
    clickPos = win.getMouse()
    while not mouseOverrectangle(clickPos, playButton):

        # Check if they clicked the Defaults button
        if mouseOverrectangle(clickPos, defaultsButton):
            # Redraw menu with default values
            undrawAll(menuInputs)
            menuInputs = intialiseMenuInputs()
            for item in menuInputs:
                item.draw(win)
        # Wait for the next click
        clickPos = win.getMouse()

    # => play button has been clicked

    # Validate menu option inputs, if any are invalid, returns defaults
    options = []
    for item in menuInputs:
        try:
            float(item.getText())   # Assumes all menu options are numeric
        except ValueError:
            for menuItem in menuInputs: # undraw menu
                menuItem.undraw()
            return menuInputs   # return default values

        # => value is valid
        options.append(eval(item.getText())) # Accept value
        item.undraw() # Remove option from menu

    play(win, options)
    return menuInputs # Return new values


# Determines whether a point is inside a rectangle
def mouseOverrectangle(mousePosition, rectangle):
    top, bottom, left, right = physics.determineRectangleBounds(rectangle)
    if mousePosition.getX() >= left \
    and mousePosition.getX() <= right \
    and mousePosition.getY() >= top \
    and mousePosition.getY() <= bottom:
        return True
    else:
        return False




################################################################################
# Code for drawing Options Menu items
################################################################################

# Draw the text label for each menu option
def drawMenuItemLabels(win):
    for i in range(len(MENU_STRINGS)):

        # Calculate position
        x = i % MENU_COLUMN_NUMBER * 200 + 100
        y = i // MENU_COLUMN_NUMBER * 80 + 50

        # Draw label
        Text(Point(x, y), MENU_STRINGS[i]).draw(win)


# Generates a list of interface components for modifying game settings
# using the default values provided
def intialiseMenuInputs():

    # Create an empty list
    menuInputs = []

    # Create and add an input for each menu item
    for i in range (len(MENU_DEFAULTS)):

        # Calculate Position
        x = i % MENU_COLUMN_NUMBER * 200 + 100
        y = i // MENU_COLUMN_NUMBER * 80 + 80

        # Create input using position and size
        tb = Entry(Point(x, y), 10)

        # Set value to default
        tb.setText(MENU_DEFAULTS[i])
        tb.setFill("white")

        # Add to input list so we can find it later
        menuInputs.append(tb)

    return menuInputs


################################################################################
# Code for drawing
################################################################################

# Drawns an X at Point pos
def drawCrosshair(win, pos):
    crosshair = Text(pos, "X")
    crosshair.setSize(10)
    crosshair.setTextColor("blue")
    crosshair.draw(win)


# Draws a button with a solid fill colour
def drawButton(win, bounds, fillColour, text, textColour):
    top, bottom, left, right = bounds
    button = Rectangle(Point(left, top), Point(right, bottom))
    button.setFill(fillColour)
    button.draw(win)
    buttonText = Text(Point((left + right) / 2, (top + bottom) / 2), text)
    buttonText.setTextColor(textColour)
    buttonText.draw(win)
    return button


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
