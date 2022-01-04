import numpy as np
# TODO: add time
# n is width
grid = []
def generateGrid(row, col, bombs):
    global grid
    grid = np.zeros((row, col))
    print(grid)

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