import numpy as np
import random
from collections import deque

# TODO: add time

key = []
user_map = []
engine_map = []
dirs = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
row = -1
col = -1
bomb = -1
tiles_revealed = 0

def backtrack():
    pass

def solve():
    for i in range(len(user_map)):
        for j in range(len(user_map[i])):
            if user_map[i][j] == True:
                if key[i][j] >= 0 and key[i][j] <= 8:
                     engine_map[i][j] = 0
                checked_tiles = []
                for dir in dirs:
                    i1, j1 = i + dir[0], j + dir[1]
                    if i1 >= 0 and i1 < len(user_map) and j1 >= 0 and j1 < len(user_map[i1]) and user_map[i1][j1] == False:
                        checked_tiles.append([i1, j1])
                if len(checked_tiles) == key[i][j]:
                    for tile in checked_tiles:
                        engine_map[tile[0]][tile[1]] = 1.0
                else:
                    backtrack()        
    print("\n")
    for i in range(len(engine_map)):
        for j in range(len(engine_map[i])):
            print("\t"+str(engine_map[i][j]), end="")
        print("\n")
    print("\n")

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
    global engine_map
    # create grid with zeroes
    key = np.zeros((row, col))
    user_map =  np.zeros((row, col), dtype=bool)
    engine_map = np.full((row, col), -1, dtype=np.double)
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
    solve()
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

def is_valid(i, j, visited):
    # in bounds
    if not (0 <= i < len(key) and 0 <= j < len(key[0])):
        return False
    # already visited
    if visited[i][j]:
        return False
    return True

def bfs(i,j):
    global tiles_revealed
    visited = np.zeros((row, col), dtype=bool)
    queue = deque()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited[i][j] = True
    queue.append((i,j))
    while queue:
        r,c = queue.popleft()
        for row_change, col_change in directions:
            neighbor_row = r + row_change
            neighbor_col = c + col_change
            if is_valid(neighbor_row, neighbor_col, visited):
                visited[neighbor_row][neighbor_col] = True
                if user_map[neighbor_row][neighbor_col] == True:
                    continue
                if key[neighbor_row][neighbor_col] == 0:
                    tiles_revealed += 1 
                    user_map[neighbor_row][neighbor_col] = True
                    queue.append((neighbor_row, neighbor_col))
                elif key[neighbor_row][neighbor_col] == -1:
                    continue
                else:
                    tiles_revealed += 1 
                    user_map[neighbor_row][neighbor_col] = True

def check_guess(i, j):
    global tiles_revealed
    if key[i][j] == -1:
        user_map[i][j] = True
        return False
    elif key[i][j] == 0:
        user_map[i][j] = True
        bfs(i,j)
        tiles_revealed += 1 
        return True
    else:
        user_map[i][j] = True
        tiles_revealed += 1 
        return True

def check_win():
    return tiles_revealed + bomb == row * col

def game_init(row, col, bomb):
    generate_grid(row, col, bomb)
    first_run = True
    while True:
        display_key()
        print("\n\n")
        display_map()
        guess_r, guess_c = prompt_guess()
        if first_run:
            while key[guess_r][guess_c] == -1:
                generate_grid(row, col, bomb)
            first_run = False
        if not check_guess(guess_r, guess_c):
            display_map()
            return False
        if check_win():
            display_key()
            break
        
    return True
    
if __name__ == "__main__":
    try:
        row = prompt("rows")
        col = prompt("columns")
        bomb = prompt("bombs")
        print("You won") if game_init(row, col, bomb) else print("L")
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')
    
    
