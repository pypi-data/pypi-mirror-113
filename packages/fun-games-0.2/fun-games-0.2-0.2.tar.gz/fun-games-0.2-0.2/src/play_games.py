from src.TicTacToe import tic_tac_toe_bot as tic_tac_toe
from src.MineSweeper import minesweeper as mine_sweeper

g_2048 = __import__('src.2048.start_play', fromlist=("src.2048"))


def get_input_for_games():
    try:
        x = input()
        if x not in ["1", "2"]:
            print("Please enter the correct command")
    except:
        print("Please enter the correct command in format 1 or 2")
        x = get_input_for_games()
    return x


def main():
    print("Welcome to the Games")
    print("Select 1 option from the below")
    print("1: 2048")
    print("2: TicTacToe")
    print("3: Mine Sweeper")
    option = get_input_for_games()
    if option == "1":
        print(" You have selected 1 and Lets Play 2048")
        g_2048.start_play()
    elif option == "2":
        print("You have selected 2 and lets Play Tic Tac Toe")
        tic_tac_toe.start_play()
    elif option == "3":
        print("You have selected 3 and lets Play Mine Sweeper")
        mine_sweeper.start_play()


if __name__ == "__main__":
    main()
