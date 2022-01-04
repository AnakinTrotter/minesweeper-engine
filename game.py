import numpy as np
import random

# TODO: add time

key = []
userMap = []
row, col, bomb = -1
def displayKey():
    for i in range(len(key)):
        for j in range(len(key[i])):
            if key[i][j] == -1:
                print("\t"+"x", end="")
            else:
                print("\t"+str(int(key[i][j])), end="")
        print("\n")

def displayMap():
    for i in range(len(userMap)):
        for j in range(len(userMap[i])):
            if userMap[i][j]:
                if key[i][j] == -1:
                    print("\t"+"x", end="")
                else:
                    print("\t"+str(key[i][j]), end="")
            else:
                print("\t"+"-", end="")
        print("\n")

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
    global key
    global userMap
    # create grid with zeroes
    key = np.zeros((row, col))
    userMap =  np.zeros((row, col), dtype=bool)
    bombs = np.asarray(generateBombs(bomb))

    for mine in bombs:
        i,j = mine

        pts = [[i-1, j], [i+1, j], [i , j+1], [i , j-1], [i-1, j+1], [i+1, j+1], [i+1, j-1], [i-1, j-1]]

        for cols in pts:
            if cols[0]>=0 and cols[0] < row and cols[1]>=0 and cols[1] < col:
                key[cols[0]][cols[1]]+=1

    for i in bombs:
        key[i[0]][i[1]] = -1

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

def gameInit():
    global row, col, bomb
    row = prompt("rows")
    col = prompt("columns")
    bomb = prompt("bombs")
    generateGrid(row, col, bomb)
    displayKey() #remove later
    print("\n")
    
    displayMap()

# function to run game: start, while true the guessing,
# function to check guess, and bfs all the way to the border zeros
# function to check if the game is over