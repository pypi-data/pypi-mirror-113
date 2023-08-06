from . import game as m
from . import logic_2048 as lg
import random,time

d={1:"a",2:"w",3:"d",4:"s"}

def automatic_play():
    board=lg.get_grid()
    m.instructions()
    while True:
        s=d[random.randint(1,4)]
        time.sleep(3)
        m.print_board(board)
        print("Enter Your Command :")
        print("Selected : ", s)
        board,key=m.play_game(board,s)
        if key=="continue":
            continue
        status = lg.check_game_status(board)
        if status == "GAME NOT OVER":
            board = lg.generate_random_2(board)
        else:
            print(status)
            break

