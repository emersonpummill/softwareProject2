''' Because of the string nature of the data input, this test only runs for gridsizes of 9x9 or less'''

import csv
import sys

data = []
gridSize = 13

badData = [['(1,2)', '(1,1)', '(2,1)'], ['(1,2)', '(1,1)', '(1,1)'], ['(2,2)', '(0,1)', '(2,1)'], 
           ['X', '(1,1)', '(2,3)'], ['X', '(1,1)', '(2,1)'], ['X', '(1,1)', '(2,1)'], ['X', '(2,1)', '(2,1)']]

with open('movement.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data.append(row)
data.pop(0)

goatFlag = 0
borderFlag = 0
for row in data:
    row = [x for x in row if x != 'X']
    diff = len(row) - len(set(row))
    if diff > 0:
        print(row)
    goatFlag = goatFlag + diff
    for location in row:
        x = int(location[1:2])
        y = int(location[3:4])
        if x == 0 or y == 0 or x == gridSize - 1 or y == gridSize -1:
            borderFlag = borderFlag + 1

if goatFlag == 0 and borderFlag == 0:
    print("\nThere are no goat or border collisions in this data!\n")
elif goatFlag == 0:
    print(f"\nThere are {borderFlag} border collisions in this data\n")
    sys.exit(1)
elif borderFlag == 0:
    print(f"\nThere are {goatFlag} goat collisions in this data\n")
    sys.exit(1)
else:
    print(f"\nThere are {goatFlag} goat collisions and {borderFlag} border collisions in this data\n")
    sys.exit(1)
