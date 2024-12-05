import random
import numpy as np
import matplotlib.pyplot as plt
import os
import imageio
import cupy as cp
import csv


# Number of Goats
numGoats = 5

# Square Grid Size
gridSize = 7

# Create empty grid array and exit position
grid = []
exitPos = []

# Create empty goat arrays
goats = []
tempGoats = []
finalGoats = []

# Create position arrays
xLocations = []
yLocations = []

# Create variables for plotting
count = 0
goatsRemaining = numGoats
filenames = []


# Create arrays of X and Y locations from the goat coordinates
def getLocations():
    xLocations.clear()
    yLocations.clear()
    for goat in goats:
        if len(goat) != 0:
            xLocations.append(goat[0])
            yLocations.append(goat[1])


# Move each goat one unit in any direction
def move(coords):
    if len(coords) == 0:
        tempGoats.append([])
    else:
        xORy = random.randint(0,1)
        dist = random.choice([-1,1])
        if xORy:
            tempGoats.append([(coords[0] + dist), coords[1]])
        else:
            tempGoats.append([coords[0], (coords[1] + dist)])


# Check for border collisions and exit position
def checkForBorderCollision():
    num = 0
    for i in range(0,len(goats)):
        if len(tempGoats[i]) != 0:
            x = tempGoats[i][0]
            y = tempGoats[i][1]
            
            # Check if goat is at border
            if x == 0 or x == gridSize - 1 or y == 0 or y == gridSize - 1:
                tempGoats[i] = goats[i]

            # Check if goat is at exit
            if x == exitPos[0] and y == exitPos[1]:
                tempGoats[i] = []
                num = num + 1
    return num


# Check for goat collisions
def checkForGoatCollision():
    for i in range(0,len(goats)):
        if len(tempGoats[i]) == 0:
            finalGoats.append([])
        else:
            if tempGoats.count(tempGoats[i]) < 2 and finalGoats.count(tempGoats[i]) == 0:
                finalGoats.append(tempGoats[i])
            else:
                finalGoats.append(goats[i])


# Create square grid
for i in range(gridSize):
    for j in range(gridSize):
        grid.append([i,j])

# Randomly select exit location
edge = random.choice([0, gridSize-1])
edgeSide = random.choice([0,1])
if edgeSide == 0:
    exitPos = [edge, random.randint(1,gridSize-2)]
if edgeSide == 1:
    exitPos = [random.randint(1,gridSize-2), edge]
print(f"Exit: [{exitPos[0]}, {exitPos[1]}]")

# Place goats within grid while avoiding borders and other goats
while len(goats) < numGoats:
    pos = random.choice(grid)
    if pos not in goats and (pos[0] != 0) and (pos[0] < gridSize - 1) and (pos[1] != 0) and (pos[1] < gridSize - 1):
        goats.append(pos)

# Update figure and axes
def updatePlot():
    fig, ax = plt.subplots()
    plt.grid(True, c="black")
    ax.set_xticks(np.arange(0, gridSize, 1))
    ax.set_yticks(np.arange(0, gridSize, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    rectangle = plt.Rectangle((0,0), gridSize - 1, gridSize - 1, fc='lightsteelblue')
    plt.gca().add_patch(rectangle)
    getLocations()
    data = plt.scatter(xLocations, yLocations, color="midnightblue")
    plt.scatter(exitPos[0], exitPos[1], color="red")
    plt.autoscale(False)
    plt.title(f"Goats Remaining: {goatsRemaining}     iterations: {count}")
    fig.savefig(f"frame_{count}.png")
    filenames.append(f"frame_{count}.png")
    plt.close()

updatePlot()

# Add list of goat positions to CSV
def formatList(list):
    row = []
    for goat in list:
        if len(goat) == 0:
            row.append("X")
        else:
            row.append(f"({goat[0]},{goat[1]})")
    with open("movement.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


# Create labels for CSV and add their initial positions
labels = []
for i in range(numGoats):
        labels.append(f"Goat {i}")
with open("movement.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(labels)
formatList(goats)


# Herd goats until they are all out of the grid
while goatsRemaining > 0:
    for goat in goats:
        move(goat)
    goatsRemaining = goatsRemaining - checkForBorderCollision()
    checkForGoatCollision()
    # print("\n\n")
    # print(goats)
    # print(tempGoats)
    formatList(finalGoats)
    # print(finalGoats)    
    goats = finalGoats
    tempGoats = []
    finalGoats = []
    count = count + 1
    getLocations()
    updatePlot() 


# Create GIF from images
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
    os.remove(filename)

dur = 10
imageio.mimsave("animation.gif", images, format='GIF', duration=dur)
