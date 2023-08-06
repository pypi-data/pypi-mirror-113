import random
from collections import deque

UNREVEALED = '?'
MINE = '*'
ZERO_NEIGHBORS = ' '


class MineSweeper:

    def __init__(self):
        self.width = 8
        self.height = 8
        self.numberOfMines = 6
        self.mineGrid = self.initialize_mine_grid()
        self.displayGrid = self.intialize_display_grid()
        print("Welcome to Mine Sweeper Game and there are 6 mines in the grid")

    def display_grid(self):
        print('  ' + ' '.join(chr(ord('a') + i) for i in range(self.width)))
        for j in range(self.height):
            print(str(j + 1) + ' ' + ' '.join(str(self.displayGrid[i][j]) for i in range(self.width)))

    def initialize_mine_grid(self):
        return [[False for _ in range(self.width)] for _ in range(self.height)]

    def intialize_display_grid(self):
        return [[UNREVEALED for _ in range(self.width)] for _ in range(self.height)]

    def getInput(self):
        try:
            a, b = input()
        except ValueError:
            print('Move format should be like: b4')
            return self.getInput()
        else:
            x = max(min(ord(a) - ord('a'), self.width - 1), 0)
            y = max(min(ord(b) - ord('1'), self.height - 1), 0)
            return x, y

    # This function is to initialize the Mine Grid
    def initializeMineGrid(self):
        for i in range(self.numberOfMines):
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            while self.mineGrid[row][col] == True:
                row = random.randint(0, self.height - 1)
                col = random.randint(0, self.width - 1)
            self.mineGrid[row][col] = True

    # If player lost we return True else return False
    def checkPlayerLost(self, x, y):
        if self.mineGrid[x][y] == True:
            return True
        return False

    # if player lost or won we will use this function to display all Mine on grid
    def displayAllMines(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.mineGrid[i][j]:
                    self.displayGrid[i][j] = MINE
        self.display_grid()

    # check all nearby mines and return the total mines around x,y
    def checkNearbyMines(self, x, y):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        mines = 0
        for neighbor in neighbors:
            new_x = x + neighbor[0]
            new_y = y + neighbor[1]
            if 0 <= new_x and new_x < self.height and 0 <= new_y and new_y < self.width:
                if self.mineGrid[new_x][new_y]:
                    mines += 1
        return mines

    # We use bfs to find nearby mines recursively and if there are 0 mines we leave it with ZERO_NEIGHBORS
    # else we will display number of mines around them
    def checkRecursivelyForMines(self, x, y):
        visited = {}
        neighbors = [(0,0), (0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        queue = deque()
        queue.append((x, y))
        mines = 0
        while queue:
            x1, y1 = queue.popleft()
            if (x1, y1) not in visited:
                visited[(x1, y1)] = True
                for neighbor in neighbors:
                    new_x = x1 + neighbor[0]
                    new_y = y1 + neighbor[1]
                    if 0 <= new_x < self.height and 0 <= new_y < self.width:
                        if not self.mineGrid[new_x][new_y]:
                            mines = self.checkNearbyMines(new_x, new_y)
                            if mines == 0:
                                self.displayGrid[new_x][new_y] = ZERO_NEIGHBORS
                                queue.append((new_x, new_y))
                            else:
                                self.displayGrid[new_x][new_y] = mines

    # will return if player won or lost the game
    def checkGameWon(self):
        unexplored = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.displayGrid[i][j] == '?':
                    unexplored += 1
                if unexplored > self.numberOfMines:
                    return False
        return self.numberOfMines == unexplored

    def play(self):
        # intialize mineGrid
        self.initializeMineGrid()
        while True:
            self.display_grid()
            x, y = self.getInput()
            if self.displayGrid[x][y]==UNREVEALED:
                # loose_condition
                if self.checkPlayerLost(x, y):
                    self.displayAllMines()
                    print("Player lost")
                    break

                # implement hint condition and calling it recursively
                self.checkRecursivelyForMines(x, y)

                # Check_game won
                if self.checkGameWon():
                    self.displayAllMines()
                    print("Player won the game")
                    break

                # self.displayGrid[x][y] = ZERO_NEIGHBORS
            else:
                print(" Please select a unrevealed grid")


def start_play():
    MineSweeper().play()
