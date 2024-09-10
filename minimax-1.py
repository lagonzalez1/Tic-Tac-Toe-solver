import random
import sys


GAME_INCOMPLETE = 0
GAME_DRAW = 1
GAME_X = 2
GAME_O = 3

X = 1
O = -1
EMPTY = 0


def evaluate_game(board):
    """
    This function tests if a specific player wins.

    Possibilities:
    Three rows    [X X X] or [O O O]
    Three cols    [X X X] or [O O O]
    Two diagonals [X X X] or [O O O]

    Arguments:
    - board: the state of the current board

    Return:
    - GAME_INCOMPLETE, GAME_DRAW, GAME_X, or GAME_O

    """
    win_states = [[board[0][0], board[0][1], board[0][2]],
                  [board[1][0], board[1][1], board[1][2]],
                  [board[2][0], board[2][1], board[2][2]],
                  [board[0][0], board[1][0], board[2][0]],
                  [board[0][1], board[1][1], board[2][1]],
                  [board[0][2], board[1][2], board[2][2]],
                  [board[0][0], board[1][1], board[2][2]],
                  [board[2][0], board[1][1], board[0][2]]]

    if [X, X, X] in win_states:
        return GAME_X
    if [O, O, O] in win_states:
        return GAME_O
    for row in board:
        for i in row:
            if i == EMPTY:
                return GAME_INCOMPLETE
    return GAME_DRAW


def print_board(board):
    """
    This function print out the current board.

    Arguments:
    - board: the state of the current board

    """
    for row in range(len(board)):
        line = ""
        for col in range(len(board[row])):
            if board[row][col] == X:
                line = line + ' X '
            elif board[row][col] == O: 
                line = line + ' O '
            else:
                line = line + "   "
            if col < 2:
                line = line + "|"
        print(line)
        if row < 2:
            print("-----------")


def O_move(board):
    best_value = 1000
    best_move = (-1, -1)

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = O  # Make a move for O
                move_value = minmax(board, 0, True)  # Evaluate this move for O
                board[row][col] = EMPTY  # Undo move
                if move_value < best_value:
                    best_value = move_value
                    best_move = (row, col)

    return best_move



def calculateScore(b, depth):
    score = 0
    r_count = 0
    for row in range(len(b)):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            return 10 - depth

    for col in range(len(b)):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            return 10 - depth

    #Check diagonal from left to right
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        return 10 - depth
    #Check dia
    if b[0][2] == b[1][1] and b[1][1] == b[2][0]: 
        return 10 - depth

    return 0
    


    
def minmax(board, depth, isMax):
    score = evaluate_game(board)

    # Check if game is already over
    if score == GAME_X:  # X wins
        return 10 - depth
    elif score == GAME_O:  # O wins
        return -10 + depth
    elif score == GAME_DRAW:  # Tie
        return 0

    if isMax:  # Maximizing player (X)
        best = -1000
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = X  # Make a move for X
                    best = max(best, minmax(board, depth + 1, False))  # Recurse with O's turn
                    board[row][col] = EMPTY  # Undo move
        return best
    else:  # Minimizing player (O)
        best = 1000
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = O  # Make a move for O
                    best = min(best, minmax(board, depth + 1, True))  # Recurse with X's turn
                    board[row][col] = EMPTY  # Undo move
        return best




    


def X_move(board):
    best_value = -1000
    best_move = (-1, -1)

    # Loop over all available cells and evaluate the best move
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = X  # Make a move for X
                move_value = minmax(board, 0, False)  # Evaluate this move
                board[row][col] = EMPTY  # Undo move
                if move_value > best_value:
                    best_value = move_value
                    best_move = (row, col)

    return best_move



board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

game_winner = GAME_INCOMPLETE

print("----------------------------")
def print_move_grid():
    for row in range(3):
        line = ""
        for col in range(3):
            line += f"({row},{col})"
            if col < 2:
                line += " | "  # Add a separator between columns
        print(line)
        if row < 2:
            print("---------")  # Add a separator between rows

# Call the function to print the grid
print_move_grid()
print("----------------------------")





while game_winner == GAME_INCOMPLETE:
    # X's move (human input)
    while True:
        try:
            r = input("Player 1 make move for row 0-2: ")
            c = input("Player 1 make move for col 0-2: ")
            row = int(r)
            col = int(c)

            # Check if the move is within bounds and on an empty spot
            if row in range(3) and col in range(3) and board[row][col] == EMPTY:
                board[row][col] = X
                break
            else:
                print("Invalid move, try again.")
        except ValueError:
            print("Please enter valid numbers between 0 and 2.")

    print_board(board)
    game_winner = evaluate_game(board)
    if game_winner != GAME_INCOMPLETE:
        break

    # O's move (AI)
    i, j = O_move(board)
    board[i][j] = O
    print("O's move:")
    print_board(board)
    game_winner = evaluate_game(board)

# Game is complete, announce winner
if game_winner == GAME_DRAW:
    print("Game was a Draw!")
elif game_winner == GAME_X:
    print("You Win!")
else:
    print("O Wins!")


