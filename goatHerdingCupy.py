import random
import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
import os
import imageio
import csv

'''
Parameters:

gridSize ~ size of one side of grid. 
            Ex. for a 4x4 grid: gridSize = 4

numGoats ~ number of goats to place in grid.
            Should be less than (gridSize-2)^2

'''
# Grid size 
gridSize = 6

# Number of Goats
numGoats = 10

# Create empty arrays for grid, goats, and exit position
grid = []
exitPos = []
goats = []
goatsRemaining = numGoats

'''

The following code blocks:
- Create square grid of size gridSize x gridSize
- Randomly select exit location on border while avoiding corners
- Place goats within grid while avoiding borders and other goats

'''
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

goats = cp.array(goats)
finalGoats = goats.copy()

''' 
The following code blocks:
- Create functions for saving data to image frames and a CSV file

'''

filenames = []
count = 0

# # Update figure and axes
# def updatePlot():
#     xAll = (goats[:,0]).tolist()
#     xLocations = [x for x in xAll if x != -1]
#     yAll = (goats[:,1]).tolist()
#     yLocations = [x for x in yAll if x != -1]
#     fig, ax = plt.subplots()
#     plt.grid(True, c="black")
#     ax.set_xticks(np.arange(0, gridSize, 1))
#     ax.set_yticks(np.arange(0, gridSize, 1))
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     ax.xaxis.set_ticks_position('none')
#     ax.yaxis.set_ticks_position('none')
#     rectangle = plt.Rectangle((0,0), gridSize - 1, gridSize - 1, fc='lightsteelblue')
#     plt.gca().add_patch(rectangle)
#     data = plt.scatter(xLocations, yLocations, color="midnightblue")
#     plt.scatter(exitPos[0], exitPos[1], color="red")
#     plt.autoscale(False)
#     plt.title(f"Goats Remaining: {goatsRemaining}     iterations: {count}")
#     fig.savefig(f"frame_{count}.png")
#     filenames.append(f"frame_{count}.png")
#     plt.close()

# updatePlot()

# Add list of goat positions to CSV
def formatList():
    row = []
    for goat in goats:
        if goat[0] == -1:
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
formatList()

'''

The following blocks:
- Move each goat one unit in any direction
- Check for exit location and remove goats if at exit
- Check for border collision and move goats back if collided
- Check for goat collisions and move goats back if collided

'''
# Move each goat one unit in any direction
def move():
    for i in range(len(goats)):
        if goats[i][0] == -1:
            tempGoats[i] = cp.array([-1,-1])
        else:
            xORy = cp.random.randint(0,2)
            dist = random.choice([-1,1])
            if xORy:
                tempGoats[i] = cp.array((goats[i][0] + dist, goats[i][1]))
            else:
                tempGoats[i] = cp.array((goats[i][0], goats[i][1] + dist))


# Check for border collisions and exit position
def checkForBorderCollision():
    global goatsRemaining
    for i in range(0,len(goats)):
        if tempGoats[i][0] != -1:
            x = tempGoats[i][0]
            y = tempGoats[i][1]

            # Check if goat is at exit
            if x == exitPos[0] and y == exitPos[1]:
                tempGoats[i] = cp.array([-1,-1])
                goatsRemaining = goatsRemaining - 1 

            # Check if goat is at border
            if x == 0 or x == gridSize - 1 or y == 0 or y == gridSize - 1:
                tempGoats[i] = goats[i]



# Check for goat collisions
def checkForGoatCollision():
    for i in range(0,len(goats)):
        if tempGoats[i][0] == -1:
            finalGoats[i] = cp.array([-1,-1])
        else:
            TGCount = 0
            FGCount = 0
            for row in tempGoats:
                if np.array_equal(row, tempGoats[i]):
                    TGCount = TGCount + 1
            for row in finalGoats:
                if np.array_equal(row, tempGoats[i]):
                    FGCount = FGCount + 1
            if TGCount < 2 and FGCount == 0:
                finalGoats[i] = tempGoats[i]
            else:
                finalGoats[i] = goats[i]

    # Keep returning collided goats to original position, and checking for new collisions
    while True:
        collisionCounter = 0
        for i in range(0,len(goats)):
            if finalGoats[i][0] != -1:
                FGCount = 0
                for row in finalGoats:
                    if np.array_equal(row, finalGoats[i]):
                        FGCount = FGCount + 1
                if FGCount > 1:
                    collisionCounter = collisionCounter + 1
                    finalGoats[i] = goats[i]
        if collisionCounter == 0:
            break

'''
The following loop runs the movement and collision functions until all goats are removed.
'''

# Repeat until all goats have exited
while goatsRemaining > 0:
    print(f"Goats Remaining: {goatsRemaining}")
    # Move each goat
    tempGoats = goats.copy()
    finalGoats.fill(-1)
    move()

    # Check for border collisions
    checkForBorderCollision()

    # Check for goat collisions
    checkForGoatCollision()
    formatList()
    # updatePlot()
    goats = finalGoats.copy()
    count += 1

# updatePlot()


# ''' 
# This code creates a GIF from the stored images, then deletes the images.
# '''
# # Create GIF from images
# images = []
# filenames.pop(0)
# for filename in filenames:
#     images.append(imageio.imread(filename))
#     os.remove(filename)

# dur = 10
# imageio.mimsave("animation.gif", images, format='GIF', duration=dur)