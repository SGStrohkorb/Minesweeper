import numpy as np
#np.random.seed(42)

class Game:

    def __init__(self, height=16, width=30, number_of_bombs=99):
        self.height, self.width, self.number_of_bombs = height, width, number_of_bombs

        empty_grid = np.zeros((self.height, self.width))
        #print(empty_grid)

        bomb_numbers_grid = empty_grid.copy()
        n = 0
        for i in range(self.height):
            for j in range(self.width):
                bomb_numbers_grid[i][j] = n
                n += 1
        print(bomb_numbers_grid)

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

        print(bomb_placement)
        print(self.bomb_grid)

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
        print(self.numbered_grid)

        self.combined_grid = empty_grid.copy()
        self.combined_grid = self.bomb_grid + self.numbered_grid
        print(self.combined_grid)

        self.visible_grid = empty_grid.copy()
        self.visible_grid -= 2
        print(self.visible_grid)

thing = Game(8, 8, 10)