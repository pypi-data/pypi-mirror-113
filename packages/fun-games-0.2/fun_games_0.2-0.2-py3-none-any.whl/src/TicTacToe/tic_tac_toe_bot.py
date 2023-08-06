player = "x"
opponent = "o"
import math
import time


# input is board and returns reward value 10 if won, -10 if lost else 0.
def calculate_reward(board):
    row_score = check_row_score(board)
    if row_score: return row_score

    column_score = check_column_score(board)
    if column_score: return column_score

    diagonal_score = check_diagonal_score(board)
    if diagonal_score: return diagonal_score

    return 0


# check all elements in the rows are equal if player won 10, lost -10
def check_row_score(board):
    for i in range(len(board)):
        if all(cell == player for cell in board[i]):
            return 10
        elif all(cell == opponent for cell in board[i]):
            return -10
    return None


# check all elements in the columns are equal if player won 10, lost -10
def check_column_score(board):
    # check all elements in the columns are equal
    for i in range(len(board[0])):
        if board[0][i] == board[1][i] == board[2][i] == player:
            return 10
        elif board[0][i] == board[1][i] == board[2][i] == opponent:
            return -10
    return None


# check all elements in the diagonal are equal if player won 10, lost -10
def check_diagonal_score(board):
    # check diagonal elements  in the columns are equal
    if board[0][0] == board[1][1] == board[2][2] == player:
        return 10
    if board[0][0] == board[1][1] == board[2][2] == opponent:
        return -10
    if board[0][2] == board[1][1] == board[2][0] == player:
        return 10
    if board[0][2] == board[1][1] == board[2][0] == opponent:
        return -10
    return None


# check if there are legal moves(atleast one empty space)
def check_legal_moves(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "_":
                return True
    return False


# calculate the best reward for the particular location in the board
def minmax(board, depth, isMax):
    reward = calculate_reward(board)

    if reward == 10:
        return 10 - depth
    if reward == -10:
        return -10 + depth

    if not check_legal_moves(board):
        return 0

    if isMax:
        bestVal = -math.inf
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "_":
                    board[i][j] = player
                    bestVal = max(bestVal, minmax(board, depth + 1, not isMax))
                    board[i][j] = "_"
        return bestVal
    else:
        bestVal = math.inf
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "_":
                    board[i][j] = opponent
                    bestVal = min(bestVal, minmax(board, depth + 1, not isMax))
                    board[i][j] = "_"
        return bestVal


# calculate the optimal move of the bot
def get_next_move(board):
    bestReward = -math.inf
    bestMove = (-1, -1)
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "_":
                board[i][j] = player
                reward = minmax(board, 0, False)
                board[i][j] = "_"
                if reward > bestReward:
                    bestReward = reward
                    bestMove = (i, j)
    return bestMove


# get input from terminal
def get_input():
    try:
        x, y = input()
        if x not in ["0", "1", "2"] or y not in ["0", "1", "2"]:
            print("please enter correct format")
            print("select 00-22 ex 00 01 02 10 11 12 20 21 22")
            x, y = get_input()
    except:
        print("please enter correct format")
        print("select 00-22 ex 00 01 02 10 11 12 20 21 22")
        x, y = get_input()
    return int(x), int(y)


# print board
def print_board(board):
    for i in range(3):
        print(board[i])


# check if player won the game or lost or its continue
def check_game_status(board):
    score = calculate_reward(board)
    if score == 10:
        print("You Lost. Better Luck next time")
        return "GAME LOST"
    elif score == -10:
        print("You Won")
        return "GAME WON"
    if not check_legal_moves(board):
        print("Game draw...")
        return "GAME DRAW"
    return "CONTINUE"


def start_play():
    board = [["_", "_", "_"],
             ["_", "_", "_"],
             ["_", "_", "_"]]
    while True:
        print_board(board)
        status = check_game_status(board)
        if status != "CONTINUE":
            break
        print("Its your Turn Make a move : select 00-22 ex 00 01 02 10 11 12 20 21 22")
        x, y = get_input()
        if board[x][y] != "_":
            print("please select an empty place")
            continue
        else:
            board[x][y] = opponent
            print_board(board)
            status = check_game_status(board)
            time.sleep(1)
            if status == "CONTINUE":
                print("Now its my turn")
                optimalMove = get_next_move(board)
                board[optimalMove[0]][optimalMove[1]] = player
            else:
                break
