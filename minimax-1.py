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
    """
    This function plays the O player (The opponent).

    Presently I have made O simply return the first valid move I find
    If you like, you can make this function match your X function
    to watch two minimax agents duke it out
    But really, this can be defined to anything you want it to do for testing.
    I will only be testing "X_move"

    Arguments:
    - board: the state of the current board

    Return:
    - a tuple (i,j) with the row, col of O's chosen move
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                return (row, col)
    print("ERROR! No Valid Move!")


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
    


    
    



def minmax(board, depth, isMax):
    score = calculateScore(board, depth)
    # Winner
    if score == 10: 
        return score
    # Tie
    if score == 0:
        return score
    # Negative score
    if score > 0:
        return score

    if isMax:
        best = -1000
        for row in range(len(board)):
            for col in range(len(board[row ])):
                if board[row][col] == EMPTY:
                    best = max( best, minmax(board, depth + 1, not isMax) )
                    board[row][col] = EMPTY
        return best
    else:
        best = 1000
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == EMPTY:
                    best = min( best, minmax(board, depth + 1, not isMax) )
                    board[row][col] = EMPTY
        
        return best



    


def X_move(board):
    # TODO: Implement the Minimax Algorithm
    #      Given an input game state, find the best move for X with the minimax algorithm
    #      For scores, you can use +10 for an X win, -10 for a O win, and 0 for a Draw
    #      In addition, in order to motivate the agent to win or lose as soon as possible, 
    #      subtract the depth of completed game state from the score. For Example:
    #
    #      If the input state is: X |   | X
    #                               |   | O
    #                               | O | 
    #
    #      Some potential completed game states might have the scores:
    #
    #      X | O | X     X Win = 10
    #        | X | O  ->             -> Score = 7
    #        | O | X     Depth = 3
    #
    #      X | X | X     X Win = 10
    #        |   | O  ->             -> Score = 9
    #        | O |       Depth = 1
    #
    #      X | O | X     Draw  = 0
    #      O | X | O  ->             -> Score = -5
    #      O | O | X     Depth = 5
    #
    #      X | O | X     O Win = -10
    #      X | O | O  ->             -> Score = -15  -> This state is actually not possible, because X always goes first
    #      O | O | X     Depth = 5                      However, in the input state I used, its actually impossible for O to win, as far as I can tell...
    #

    defaultValue = - 100
    # START FILLER CODE, just picks first valid move!
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                move = minmax(board, 0, False) # Assume is not max since O will make the next move
                if move > defaultValue:
                    defaultValue = move
                    return (row, col)


    print("ERROR! No Valid Move!")
    # END FILLER CODE


board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

game_winner = GAME_INCOMPLETE
# Game Loop
while game_winner == GAME_INCOMPLETE:
    i, j = X_move(board)
    board[i][j] = X
    print_board(board)
    game_winner = evaluate_game(board)
    if game_winner != GAME_INCOMPLETE:
        break
    i, j = O_move(board)
    board[i][j] = O
    print_board(board)
    game_winner = evaluate_game(board)

# Game is complete, announce winner
if game_winner == GAME_DRAW:
    print("Game was a Draw!")
elif game_winner == GAME_X:
    print("X Wins!")
else:
    print("O Wins!")
