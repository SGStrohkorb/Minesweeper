import numpy as np
np.random.seed(42)

height = 8#16
width = 8#30
number_of_bombs = 4#99

empty_grid = np.zeros((height, width))
#print(empty_grid)

numbered_grid = empty_grid.copy()
n = 0
for i in range(height):
    for j in range(width):
        numbered_grid[i][j] = n
        n += 1
print(numbered_grid)

bomb_grid = empty_grid.copy()
#Make excessive number of bombs because randint doesn't create a set
#Then use only the number of bombs
bomb_placement = np.random.randint(0, height*width, size=number_of_bombs*2)
#I know this isn't the most efficient way to do this, it just makes sense to me
for i in range(number_of_bombs):
    bomb = bomb_placement[i]
    x, y = np.where(numbered_grid == bomb)
    x, y = x[0], y[0]
    bomb_grid[x, y] = -1
    print(bomb, x, y)

#print(bomb_placement)
print(bomb_grid)
