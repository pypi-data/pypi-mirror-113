import random

def get_grid():
    board=[]
    for i in range(4):
        board.append([0]*4)
    generate_random_2(board)
    return board

def check_zero(board):
    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                return True
    return False

def generate_random_2(board):
    r=random.randint(0,3)
    c=random.randint(0,3)
    if check_zero(board):
        while board[r][c]!=0:
            r = random.randint(0, 3)
            c = random.randint(0, 3)
        board[r][c]=2
    return board

def compress(board):
    new_board=[]
    for i in range(4):
        new_board.append([0]*4)
    changed=False
    for i in range(4):
        start=0
        for j in range(4):
            if board[i][j]!=0:
                new_board[i][start]=board[i][j]
                if j!=start:
                    changed=True
                start+=1
    return changed, new_board

def merge(board):
    changed=False
    for i in range(4):
        for j in range(3):
            if board[i][j]!=0:
                if board[i][j]==board[i][j+1]:
                    board[i][j]=board[i][j]*2
                    board[i][j+1]=0
                    changed=True
    return changed,board

def move_left(board):
    changed1,board=compress(board)
    changed2, board = merge(board)
    if changed1 or changed2:
        changed, board = compress(board)
    return board

def reverse(board):
    for i in range(4):
        board[i]=board[i][::-1]
    return board

def transpose(board):
    new_board=[]
    for i in range(4):
        new_board.append([0]*4)
        for j in range(4):
            new_board[i][j]=board[j][i]
    return new_board

def move_right(board):
    board=reverse(board)
    board=move_left(board)
    board=reverse(board)
    return board

def move_up(board):
    board=transpose(board)
    board=move_left(board)
    board=transpose(board)
    return board

def move_down(board):
    board = transpose(board)
    board = move_right(board)
    board = transpose(board)
    return board

def check_game_status(board):
    for i in range(4):
        for j in range(4):
            if board[i][j]==2048:
                return "GAME WON"

    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                return "GAME NOT OVER"

    for i in range(4):
        for j in range(3):
            if board[i][j]!=0:
                if board[i][j]==board[i][j+1]:
                    return "GAME NOT OVER"
                if board[j][i]==board[j+1][i]:
                    return "GAME NOT OVER"

    return "LOST"
