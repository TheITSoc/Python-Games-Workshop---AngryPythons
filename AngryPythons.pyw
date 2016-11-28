from graphics import *
import physics
import shapeGen

# Below are some constants that are globabaly visible to make the code simpler
# Note that in Python, a tuple is a list that cannot be modified

# Tuple of the description text for each menu option
MENU_STRINGS = (
                "Number of targets",
                "Number of obstacles",
                "Number of tries",
                "FPS",
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
                 "60", "12", "0.15", "0.5", "9.8",
                 "10", "30", "70", "300")

# Number of columns in the menu (must be even)
MENU_COLUMN_NUMBER = 4


## Colours, specified as HEX codes
#COLOURS = {
#    'red'       : '#ef3b3b',
#    'gold'      : '#ecef3b',
#    'green'     : '#13c625',
#}



# Program entry point, opens window and displays options menu
def main(width, height):

    win = GraphWin("PyBirds", width, height)
    menuInputs = intialiseMenuInputs()
    while True:
        menuInputs = menu(win, menuInputs)


# Run the game with the specified parameters
def play(win, options):

    # Load options from menu
    targetNumber = options[0]
    obstacleNumber = options[1]
    triesLeft = options[2]
    physicsConstants = options[3:8]
    obstacleDimensionRanges = options[8:12]

    bearingPoint = Point(win.getWidth() / 10, win.getHeight() * 4 / 5) # Top of catapult

    # Draw constants and UI
    drawBackdrop(win)
    drawScenery(win, bearingPoint)
    menuButton = drawButton(win, [0, 20, 0, 80], "red", "Menu", "gold")
    triesLeftDisplay = Text(Point(100, 10), triesLeft)
    triesLeftDisplay.draw(win)

    # Generate level
    obstacles = shapeGen.genRandomObstacles(win, obstacleNumber, obstacleDimensionRanges)
    if obstacles == []:
        showMessage(win, "Failed to place obstacles!", "red", "orange")
        return
    targets = shapeGen.genRandomTargets(win, targetNumber, obstacles)
    if targets == []:
        showMessage(win, "Failed to place targets!", "red", "orange")
        return

    # Testing - uncomment below for hard-coded level layout
    #obstacles = shapeGen.setObstacles(win)
    #targets = shapeGen.setTargets(win)

    # Listen for user interaction
    while triesLeft > 0 and len(targets) > 0:

        # Check for non game related clicking
        clickPos = Point(1000, 0) #Invalid data for while
        while clickPos.getX() > win.getWidth() / 10: # Out of bounds (right of catapult)
            clickPos = win.getMouse()
        if mouseOverrectangle(clickPos, menuButton):
            return # End game and return to menu

        # => valid position to fire from

        # Update tries left
        triesLeft = triesLeft - 1
        triesLeftDisplay.setText(triesLeft)

        # Run simulation
        physics.simulateProjectile(win, bearingPoint, clickPos, obstacles, targets, physicsConstants)

    # => game finished (either no tries or targets remaining)

    won = len(targets) == 0

    if won:
        showMessage(win, "You win", "darkgreen", "yellow")
    else:
        showMessage(win, "Out of tries", "red", "orange")

    win.getMouse()
    undrawAll(targets)
    undrawAll(obstacles)
    return


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

    # Wait for the user to click
    clickPos = win.getMouse()

    # Keep looping till they click within the Play button
    while not mouseOverrectangle(clickPos, playButton):

        # Check if they clicked the Defaults button
        if mouseOverrectangle(clickPos, defaultsButton):
            # Redraw menu with default values
            for item in menuInputs:
                item.undraw()
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
def drawScenery(win, bearingPoint):
    # Draw power rings
    outerRingRadius = win.getWidth() / 8
    # Draw a red ring at full size
    redRing = Circle(bearingPoint, outerRingRadius)
    redRing.setFill("red")
    redRing.draw(win)
    # Draw a yellow ring on top, 2/3 the size of the red ring
    yellowRing = Circle(bearingPoint, outerRingRadius * 2 / 3)
    yellowRing.setFill("yellow")
    yellowRing.draw(win)
    # Draw a green ring on top, 1/3 the size of the red ring
    greenRing = Circle(bearingPoint, outerRingRadius / 3)
    greenRing.setFill("green")
    greenRing.draw(win)

    # Draw catapult
    catapultBottomPos = Point(bearingPoint.getX() - 5, win.getHeight())
    catapult = Rectangle(bearingPoint, catapultBottomPos)
    catapult.setFill("brown")
    catapult.draw(win)

    # Draw the sky
    skyTopLeft = Point(win.getWidth() / 10, 0)
    skyBottomRight = Point(win.getWidth(), win.getHeight() + 10)
    sky = Rectangle(skyTopLeft, skyBottomRight)
    sky.setFill("lightblue")
    sky.draw(win)


main(1200, 500)
