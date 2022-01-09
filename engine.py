import numpy as np
from collections import deque

from numpy.core.fromnumeric import shape

dirs = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

# edit this board to change the test
board = np.array(
    [
        [1, None, None, None, None, None, 1],
        [1, 2, 4, None, 4, 2, 1],
        [0, 0, 1, None, 1, 0, 0],
    ]
)

m, n = len(board), len(board[0])


"""Attempts to find a safe square and resorts to probabilities if one cannot be found"""

def solve():
    global board, m, n
    for i in range(m):
        for j in range(n):
            if board[i][j] is None or board[i][j] <= 0 or board[i][j] > 8:
                continue
            open_tiles = []
            for dir in dirs:
                i1, j1 = i + dir[0], j + dir[1]
                if i1 >= 0 and i1 < m and j1 >= 0 and j1 < n:
                    if board[i1][j1] is None and can_put_mine(i1, j1):
                        open_tiles.append([i1, j1])
            # handle the trivial case
            if len(open_tiles) == board[i][j]:
                for tile in open_tiles:
                    # max legit tile is 8, anything higher is mine
                    board[tile[0]][tile[1]] = 999
                    # subtract 1 from all tiles adjacent of a mine
                    add_adj(tile[0], tile[1], -1)
                    return
    # handle nontrivial cases
    visited = np.zeros((m, n), dtype=bool)
    for i in range(m):
        for j in range(n):
            if visited[i][j] == False and board[i][j] is None and is_border_tile(i, j):
                edge = []
                q = deque()
                q.appendleft((i, j))
                edge.append((i, j))
                visited[i][j] = True
                # bfs to get the border we want to permute
                while q:
                    r, c = q.popleft()
                    for dir in dirs:
                        i1, j1 = r + dir[0], c + dir[1]
                        if i1 >= 0 and i1 < m and j1 >= 0 and j1 < n and board[i1][j1] is None:
                            if visited[i1][j1] == False and is_border_tile(i1, j1):
                                q.appendleft((i1, j1))
                                visited[i1][j1] = True
                                edge.append((i1, j1))
                # use backtracking to get array of board permutations
                solutions = []
                backtrack(0, edge, solutions)
                if len(solutions) == 1:
                    board = solutions[0].copy()
                else:
                    # count the mines on each tile for each solution
                    counts = np.zeros((len(edge)), dtype=int)
                    for solution in solutions:
                        for x in range(len(edge)):
                            if solution[edge[x][0]][edge[x][1]] is not None:
                                if solution[edge[x][0]][edge[x][1]] > 8:
                                    counts[x] += 1
                    ans = 0
                    for x in range(len(counts)):
                        # if a tile is a mine in every case then mark it and we are done
                        if counts[x] == len(solutions):
                            board[edge[x][0]][edge[x][1]] = 999
                            add_adj(edge[x][0], edge[x][1], -1)
                            return
                        if counts[x] > counts[ans]:
                            ans = x
                    # finally resort to guessing
                    gr, gc = edge[ans]
                    board[gr][gc] = 999
                    add_adj(edge[x][0], edge[x][1], -1)

"""Permutes a border of potential mines and saves the valid board states"""

def backtrack(idx, arr, ans):
    global board
    if idx == len(arr):
        if is_border_solved(arr):
            ans.append(board.copy())
        return
    i, j = arr[idx]
    if can_put_mine(i, j):
        # Case 1: place mine
        board[i][j] = 999
        add_adj(i, j, -1)
        backtrack(idx + 1, arr, ans)
        # undo last step (backtrack)
        board[i][j] = None
        add_adj(i, j, 1)
    # Case 2: skip tile
    backtrack(idx + 1, arr, ans)


"""Checks if a given array of border tiles is properly solved"""

def is_border_solved(arr):
    global board, m, n
    for tile in arr:
        i, j = tile
        for dir in dirs:
            i1, j1 = i + dir[0], j + dir[1]
            if i1 >= 0 and i1 < m and j1 >= 0 and j1 < n:
                if board[i1][j1] is not None and board[i1][j1] >= 1 and board[i1][j1] <= 8:
                    return False
    return True


"""Checks if a given tile is touching any revealed tiles"""

def is_border_tile(i, j):
    global board, m, n
    for dir in dirs:
        i1, j1 = i + dir[0], j + dir[1]
        if i1 >= 0 and i1 < m and j1 >= 0 and j1 < n:
            if board[i1][j1] is not None and board[i1][j1] > 0 and board[i1][j1] <= 8:
                return True
    return False


"""Checks if placing a mine on the given tile creates a legal board state"""

def can_put_mine(i, j):
    global board, m, n
    for dir in dirs:
        i1, j1 = i + dir[0], j + dir[1]
        if i1 >= 0 and i1 < m and j1 >= 0 and j1 < n and board[i1][j1] is not None:
            if board[i1][j1] <= 0:
                return False
    return True


"""Adds k to all tiles adjacent to the given tile"""

def add_adj(i, j, k):
    global board, m, n
    for dir in dirs:
        i1, j1 = i + dir[0], j + dir[1]
        if i1 >= 0 and i1 < m and j1 >= 0 and j1 < n and board[i1][j1] is not None:
            board[i1][j1] += k


"""Prints the current global board state"""

def print_board():
    global board
    print("\n")
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                print("\t?", end="")
            elif board[i][j] > 8:
                print("\t🚩", end="")
            else:
                print("\t" + str(board[i][j]), end="")
        print("\n")


"""Plays the best move for x turns and updates the board"""

def do_turns(x):
    initial_board = board.copy()
    print("\nTURN 0:\n")
    print_board()
    for i in range(1, x + 1):
        print("\nTURN " + str(i) + ":\n")
        solve()
        print_board()
    print("\nLOCATIONS OF MINES:\n")
    mines = []
    for i in range(m):
        for j in range(n):
            if board[i][j] is not None and board[i][j] > 8:
                mines.append((i, j))
    print(mines)

if __name__ == "__main__":
    print("\n\n\n")
    do_turns(6)
    print("\n\n\n")
