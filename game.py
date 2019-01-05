import colorama
from colorama import Fore, Style #Colors: 'BLACK', 'BLUE', 'CYAN', 'GREEN', 'LIGHTBLACK_EX', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX', 'LIGHTGREEN_EX', 'LIGHTMAGENTA_EX', 'LIGHTRED_EX', 'LIGHTWHITE_EX', 'LIGHTYELLOW_EX', 'MAGENTA', 'RED', 'RESET', 'WHITE', 'YELLOW'
import numpy as np

colorama.init()
np.random.seed(42)

class Game:
    def __init__(self, height=16, width=30, number_of_bombs=99):
        self.height, self.width, self.number_of_bombs = height, width, number_of_bombs
        self.done = False

        empty_grid = np.zeros((self.height, self.width))
        #print(empty_grid)

        bomb_numbers_grid = empty_grid.copy()
        n = 0
        for i in range(self.height):
            for j in range(self.width):
                bomb_numbers_grid[i][j] = n
                n += 1
        #print(bomb_numbers_grid)

        self.bomb_grid = empty_grid.copy()
        #Make excessive number of bombs because randint doesn't create a set
        #Then use only the number of bombs
        bomb_placement = np.random.randint(0, self.height*self.width, size=self.number_of_bombs*2)
        bomb_placement = list(set(bomb_placement))
        bomb_coordinates = []
        #I know this isn't the most efficient way to do this, it just makes sense to me
        for i in range(self.number_of_bombs):
            bomb = bomb_placement[i]
            x, y = np.where(bomb_numbers_grid == bomb)
            x, y = x[0], y[0]
            self.bomb_grid[x, y] = -1
            bomb_coordinates.append([x, y])
            #print(bomb, x, y)

        #print(bomb_placement)
        #print(self.bomb_grid)

        self.numbered_grid = empty_grid.copy()
        for x, y in bomb_coordinates:
            #print(x, y)
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    if [i, j] in bomb_coordinates: #if coordinate is a bomb
                        #print(x, y, i, j, "bomb")
                        pass
                    elif (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                        #print(x, y, i, j, "grid")
                        pass
                    else:
                        self.numbered_grid[i, j] += 1
                        #print(x, y, i, j, "true")
        #print(self.numbered_grid)

        self.combined_grid = empty_grid.copy()
        self.combined_grid = self.bomb_grid + self.numbered_grid
        print(self.combined_grid)

        self.visible_grid = empty_grid.copy()
        self.visible_grid -= 2
        #print(self.visible_grid)

        self.actions = empty_grid.copy()
        self.actions += 1

    def left_mouse_click(self, x, y):
        """When the player 'clicks' on a point"""
        value = self.combined_grid[x, y]
        action_value = self.actions[x, y]
        #print(value, "HI")

        invalid_action = False
        if value == -1:
            self.done = True
            self.visible_grid[x, y] = -3
        elif value != 0 and action_value == 1:
            self.visible_grid[x, y] = value
            self.actions[x, y] = 0
        elif value != 0 and action_value == 0:
            invalid_action = True
        elif value == 0 and action_value == 1:
            #print(x, y, "X, Y")
            points = [[x,y]]
            for X, Y in points:
                #print(X, Y, points, "start")
                for i in [X-1, X, X+1]:
                    for j in [Y-1, Y, Y+1]:
                        if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                            pass
                        elif self.combined_grid[i, j] == -1: #if coordinate is a bomb
                            pass
                        else:
                            if self.combined_grid[i,j] == 0:
                                if [i,j] not in points:
                                    points.append([i,j])
                                    #print([i,j], points, "Append")
                            self.visible_grid[i, j] = self.combined_grid[i, j]
                #del points[0]
        print(self)
        return invalid_action

    def __str__(self):
        if -3 in self.visible_grid:
            grid = self.combined_grid
        else:
            grid = self.visible_grid

        for row in grid:
            for i, element in enumerate(row):
                if i != (len(row)-1):
                    end = " "
                else:
                    end = "\n"

                if element == -2:
                    print(Fore.WHITE + '0', end=end)
                elif element == 0:
                    print(" ", end=end)
                elif element == 1:
                    print(Fore.BLUE + '1', end=end)
                elif element == 2:
                    print(Fore.GREEN + '2', end=end)
                elif element == 3:
                    print(Fore.LIGHTRED_EX + '3', end=end)
                elif element == 4:
                    print(Fore.LIGHTMAGENTA_EX + '4', end=end)
                elif element == 5:
                    print(Fore.RED + '5', end=end)
                elif element == 6:
                    print(Fore.CYAN + '6', end=end)
                elif element == 7:
                    print(Fore.LIGHTGREEN_EX + '7', end=end)
                elif element == 8:
                    print(Fore.LIGHTYELLOW_EX + '8', end=end)
                elif element == -1:
                    print(Fore.RED + 'B', end=end)
                else:
                    print(element, end=end)
        return ""

thing = Game(8, 8, 10)
thing.left_mouse_click(0,0)
thing.left_mouse_click(0,4)
