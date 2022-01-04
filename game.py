import numpy as np
import random

# TODO: add time

grid = []
def generateBombs(bomb):
    bombs = set()
    for i in range(bomb):
        bombRow = random.randint(0,row-1)
        bombCol = random.randint(0, col-1)
        while(bombRow, bombCol) in bombs:
            bombRow = random.randint(0,row-1)
            bombCol = random.randint(0, col-1)
        bombs.add((bombRow, bombCol))
    return list(bombs)

def generateGrid(row, col, bomb):
    global grid
    # create grid with zeroes
    grid = np.zeros((row, col))
    bombs = np.asarray(generateBombs(bomb))

    for mine in bombs:
        i= mine[0]
        j= mine[1]

        pts = [[i-1, j], [i+1, j], [i , j+1], [i , j-1], [i-1, j+1], [i+1, j+1], [i+1, j-1], [i-1, j-1]]

        for cols in pts:
            if cols[0]>=0 and cols[0] < row and cols[1]>=0 and cols[1] < col:
                grid[cols[0]][cols[1]]+=1

    for i in bombs:
        grid[i[0]][i[1]] = -1
        

def prompt(promptType):
    while True:
        try:
            value = int(input("Enter number of " + promptType + ":  "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if promptType != "bombs" and value < 3:
            print("Sorry, your response must be greater than 3.")
            continue
        elif promptType == "bombs":
            global row
            global col
            if value < row*col and value > 0:
                break
            print("Sorry, your response is invalid.")
            continue
        else:
            break
    return value

row = prompt("rows")
col = prompt("columns")
bomb = prompt("bombs")
generateGrid(row, col, bomb)
print(grid)