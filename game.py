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
                print("\t"+"💣", end="")
            else:
                print("\t"+str(int(key[i][j])), end="")
        print("\n")

def display_map():
    for i in range(len(user_map)):
        for j in range(len(user_map[i])):
            if user_map[i][j]:
                if key[i][j] == -1:
                    print("\t"+"💥", end="")
                else:
                    print("\t"+str(int(key[i][j])), end="")
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

def isValid(i, j, visited):
    # in bounds
    if not (0 <= i < len(key) and 0 <= j < len(key[0])):
        return False
    # already visited
    if (i, j) in visited:
        return False
    return True
def bfs(i,j):
    visited = []
    queue = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited.append((i,j))
    queue.append((i,j))

    while queue:
        r,c = queue.pop(0)
        for row_change, col_change in directions:
            neighbor_row = r + row_change
            neighbor_col = c + col_change
            if isValid(neighbor_row, neighbor_col, visited):
                visited.append((neighbor_row, neighbor_col))
                # check what value it is, if its a zero u add to the queue, if its -1 dont show, if its a number show and dont add to queue
                if key[neighbor_row][neighbor_col] == 0:
                    user_map[neighbor_row][neighbor_col] = True
                    queue.append((neighbor_row, neighbor_col))
                elif key[neighbor_row][neighbor_col] == -1:
                    continue
                else:
                    user_map[neighbor_row][neighbor_col] = True


def check_guess(i, j):
    if key[i][j] == -1:
        user_map[i][j] = True
        return False
    elif key[i][j] == 0:
        # bfs here
        bfs(i,j)
        print("hi")
        return True
    else:
        user_map[i][j] = True
        return True

def check_game_state(guesses):
    return guesses + bomb < row * col

def game_init():
    global row, col, bomb
    row = prompt("rows")
    col = prompt("columns")
    bomb = prompt("bombs")
    game_state = True
    guesses = 0
    generate_grid(row, col, bomb)

    while game_state:
        display_map()
        guess_x, guess_y = prompt_guess()
        if not check_guess(guess_x, guess_y):
            display_map()
            return False
        guesses += 1
        game_state = check_game_state(guesses)
        
    return True
    
if __name__ == "__main__":
    print("You won") if game_init() else print("L")
    display_key()
# function to run game: start, while true the guessing,
# function to check guess, and bfs all the way to the border zeros
# function to check if the game is over