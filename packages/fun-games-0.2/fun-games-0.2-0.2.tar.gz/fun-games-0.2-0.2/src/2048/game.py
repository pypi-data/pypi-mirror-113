from . import logic_2048 as lg

def print_board(board):
    print("-------------")
    print(board[0])
    print(board[1])
    print(board[2])
    print(board[3])

def instructions():
    print(" Click w to move up")
    print(" Click s to move down")
    print(" Click d to move right")
    print(" click a to move left")

def play_game(board,ins):
    if ins == "w":
        board = lg.move_up(board)
    elif ins == "s":
        board = lg.move_down(board)
    elif ins == "a":
        board = lg.move_left(board)
    elif ins == "d":
        board = lg.move_right(board)
    else:
        print("Please enter the correct command")
        return board,"continue"
    return board,""


def start():
    board=lg.get_grid()
    instructions()
    while True:
        print_board(board)
        print("Enter Your Command :")
        ins = input()
        board,key=play_game(board,ins)
        if key=="continue":
            continue
        status = lg.check_game_status(board)
        if status == "GAME NOT OVER":
            board = lg.generate_random_2(board)
        else:
            print(status)
            break

