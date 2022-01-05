import numpy as np
import random

# TODO: add time

key = []
user_map = []
row = -1
col = -1
bomb = -1
def display_key():
    for i in range(len(key)):
        for j in range(len(key[i])):
            if key[i][j] == -1:
                print("\t"+"x", end="")
            else:
                print("\t"+str(int(key[i][j])), end="")
        print("\n")

def display_map():
    for i in range(len(user_map)):
        for j in range(len(user_map[i])):
            if user_map[i][j]:
                if key[i][j] == -1:
                    print("\t"+"x", end="")
                else:
                    print("\t"+str(key[i][j]), end="")
            else:
                print("\t"+"-", end="")
        print("\n")

def generate_bombs(bomb):
    bombs = set()
    for i in range(bomb):
        bomb_row = random.randint(0,row-1)
        bomb_col = random.randint(0, col-1)
        while(bomb_row, bomb_col) in bombs:
            bomb_row = random.randint(0,row-1)
            bomb_col = random.randint(0, col-1)
        bombs.add((bomb_row, bomb_col))
    return list(bombs)

def generate_grid(row, col, bomb):
    global key
    global user_map
    # create grid with zeroes
    key = np.zeros((row, col))
    user_map =  np.zeros((row, col), dtype=bool)
    bombs = np.asarray(generate_bombs(bomb))

    for mine in bombs:
        i,j = mine

        pts = [[i-1, j], [i+1, j], [i , j+1], [i , j-1], [i-1, j+1], [i+1, j+1], [i+1, j-1], [i-1, j-1]]

        for cols in pts:
            if cols[0]>=0 and cols[0] < row and cols[1]>=0 and cols[1] < col:
                key[cols[0]][cols[1]]+=1

    for i in bombs:
        key[i[0]][i[1]] = -1

def prompt(prompt_type):
    while True:
        try:
            value = int(input("Enter number of " + prompt_type + ":  "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if prompt_type != "bombs" and value < 3:
            print("Sorry, your response must be greater than 3.")
            continue
        elif prompt_type == "bombs":
            global row
            global col
            if value < row*col and value > 0:
                break
            print("Sorry, your response is invalid.")
            continue
        else:
            break
    return value

def prompt_guess():
    while True:
        try:
            x = int(input("Enter row (0 index):  "))
            y = int(input("Enter column (0 index):  "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if x < 0 or x >= row:
            print("input out of bounds")
            continue
        elif y < 0 or y >= col:
            print("input out of bounds")
            continue
        else:
            if user_map[x][y] == True:
                print("Location already cleared")
                continue
            break
    return x, y

def check_guess(i, j):
    # bfs my way out check to see if its bomb
    print(i, j)
    return False

def check_game_state(guesses):
    return guesses + bomb == row * col

def game_init():
    global row, col, bomb
    row = prompt("rows")
    col = prompt("columns")
    bomb = prompt("bombs")
    game_state = True
    guesses = 0
    generate_grid(row, col, bomb)
    
    while game_state:
        guess_x, guess_y = prompt_guess()
        if not check_guess(guess_x, guess_y):
            print("you lost L")
            display_map()
            break
        guesses += 1
        game_state = check_game_state(guesses)
        display_map()

    
if __name__ == "__main__":
    game_init()
# function to run game: start, while true the guessing,
# function to check guess, and bfs all the way to the border zeros
# function to check if the game is over