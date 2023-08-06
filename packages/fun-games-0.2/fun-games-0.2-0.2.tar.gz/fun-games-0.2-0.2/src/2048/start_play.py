from . import game as g

from . import game_bot_automaticplay as gba

def start_play():
    while (True):
        print("Select 1 for single player")
        print("Select 2 for a demo to see a bot play")
        print("Select the option to play :")
        ch=input()
        if ch=='1':
            g.start()
        elif ch=='2':
            gba.automatic_play()
        else:
            print("Wrong option. Please Type the proper option")
            continue
        break