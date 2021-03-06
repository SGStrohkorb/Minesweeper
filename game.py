import colorama
from colorama import Fore, Style #Colors: 'BLACK', 'BLUE', 'CYAN', 'GREEN', 'LIGHTBLACK_EX', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX', 'LIGHTGREEN_EX', 'LIGHTMAGENTA_EX', 'LIGHTRED_EX', 'LIGHTWHITE_EX', 'LIGHTYELLOW_EX', 'MAGENTA', 'RED', 'RESET', 'WHITE', 'YELLOW'
import numpy as np
from itertools import permutations

colorama.init()
np.random.seed(42) #need to remove later

class Game:
    def __init__(self, height=16, width=30, number_of_bombs=99, visual_updates=True):
        self.height, self.width, self.number_of_bombs = height, width, number_of_bombs
        self.visual_updates = visual_updates
        self.done = False
        self.win = False

        self.empty_grid = np.zeros((self.height, self.width))
        #print(self.empty_grid)

        bomb_numbers_grid = self.empty_grid.copy()
        n = 0
        for i in range(self.height):
            for j in range(self.width):
                bomb_numbers_grid[i][j] = n
                n += 1
        #print(bomb_numbers_grid)

        self.bomb_grid = self.empty_grid.copy()
        bomb_placement = []
        bomb_coordinates = []
        #I know this isn't the most efficient way to do this, it just makes sense to me
        for i in range(self.number_of_bombs):
            bomb = np.random.randint(0, self.height*self.width)
            while bomb in bomb_placement:
                bomb = np.random.randint(0, self.height*self.width)
            x, y = np.where(bomb_numbers_grid == bomb)
            x, y = x[0], y[0]
            self.bomb_grid[x, y] = -1
            bomb_coordinates.append([x, y])
            bomb_placement.append(bomb)
            #print(bomb, x, y)

        #print(bomb_placement)
        #print(self.bomb_grid)

        self.numbered_grid = self.empty_grid.copy()
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
        self.combined_grid = self.empty_grid.copy()
        self.combined_grid = self.bomb_grid + self.numbered_grid
        #print(self.combined_grid)

        self.visible_grid = self.empty_grid.copy()
        self.visible_grid -= 2
        #print(self.visible_grid)

        self.actions = self.empty_grid.copy()
        self.actions += 1

        self.tmp_solve_grid = self.empty_grid.copy()

    def left_mouse_click(self, x, y):
        """When the player 'clicks' on a point"""
        value = self.combined_grid[x, y]
        action_value = self.actions[x, y]
        #print(value, "HI")

        invalid_action = False
        if value == -1:
            self.done = True
            self.win = False
            self.visible_grid[x, y] = -3
            self.actions = self.empty_grid.copy()
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
        if self.visual_updates:
            print(self)

        if self.is_done():
            if self.win:
                print("Congration! You done it!")
                return True
            else:
                print("You lost")
                return True
        return invalid_action

    def right_mouse_click(self, x, y):
        value = self.combined_grid[x, y]
        visible_value = self.visible_grid[x, y]

        if visible_value == -2:
            self.visible_grid[x, y] = -4
        elif visible_value == -4:
            self.visible_grid[x, y] -= 1
        elif visible_value == -5:
            self.visible_grid[x, y] = -2

        if self.is_done():
            if self.win:
                print("Congration! You done it!")
                return True
            else:
                print("You lost")
                return True

        if self.visual_updates:
            print(self)

    def is_done(self):
        #print(self.visible_grid)
        contradiction = False
        for X in range(self.height):
            for Y in range(self.width):
                tmp_needed_number_of_bombs = self.visible_grid[X, Y]
                tmp_actual_number_of_bombs = 0
                tmp_number_of_uncovered_spots = 0
                for i in [X-1, X, X+1]:
                    for j in [Y-1, Y, Y+1]:
                        if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                            pass
                        else:
                            if self.visible_grid[i,j] == -4:
                                tmp_actual_number_of_bombs += 1
                            elif self.visible_grid[i,j] == -3:
                                self.done = True
                                self.win = False
                                return True
                            elif self.visible_grid[i,j] == -2:
                                tmp_number_of_uncovered_spots += 1
                #print(tmp_number_of_uncovered_spots, X, Y, i, j)

                if ((tmp_needed_number_of_bombs != tmp_actual_number_of_bombs) and (tmp_needed_number_of_bombs > 0)) or (tmp_number_of_uncovered_spots != 0):
                    contradiction = True

        
        if contradiction:
            return False
        else:
            self.done = True
            self.win = True
            return True
        
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
                elif element == -4:
                    print(Fore.WHITE+ chr(1168), end=end)
                    #print(Fore.WHITE+ '*', end=end)
                elif element == -5:
                    print(Fore.LIGHTBLACK_EX + chr(191), end=end)
                    #print(Fore.LIGHTBLACK_EX + '?', end=end)
                else:
                    print(element, end=end)
        return Fore.RESET + ''

    def clear_step(self):
        cleared = 0

        for X in range(self.height):
            for Y in range(self.width):
                if self.visible_grid[X,Y] >= 1:
                    number_of_bombs_local = self.visible_grid[X,Y]
                    possible_bombs = 0
                    known_bombs = 0
                    #print(number_of_bombs_local)
                    for i in [X-1, X, X+1]:
                        for j in [Y-1, Y, Y+1]:
                            if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                pass
                            elif self.visible_grid[i,j] in [-2, -5]:
                                possible_bombs += 1
                            elif self.visible_grid[i,j] == -4:
                                known_bombs += 1
                    #print(possible_bombs, number_of_bombs_local, X, Y)
                    #print()

                    if (known_bombs == number_of_bombs_local) and number_of_bombs_local != 0 and possible_bombs > 0:
                        #print("Clearing", X, Y)
                        cleared += 1
                        for i in [X-1, X, X+1]:
                            for j in [Y-1, Y, Y+1]:
                                if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                    pass
                                elif self.visible_grid[i,j] == -2:
                                    self.left_mouse_click(i,j)
        return bool(cleared)

class Solving_Game(Game):

    def __init__(self, height=16, width=30, number_of_bombs=99, visual_updates=True):
        super().__init__(height, width, number_of_bombs, visual_updates)

    def solve_step(self):
        old_visible_grid = self.visible_grid.copy()
        #print(self.visible_grid)
        #print(self.combined_grid)

        #print()

        if_break = False
        for X in range(self.height):
            for Y in range(self.width):
                if self.visible_grid[X,Y] >= 1:
                    number_of_bombs_local = self.visible_grid[X,Y]
                    possible_bombs = 0
                    known_bombs = 0
                    #print(number_of_bombs_local)
                    for i in [X-1, X, X+1]:
                        for j in [Y-1, Y, Y+1]:
                            if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                pass
                            #elif self.visible_grid[i,j] == -2:
                                #possible_bombs += 0
                            elif self.visible_grid[i,j] in [-2, -5]:
                                possible_bombs += 1
                            elif self.visible_grid[i,j] == -4:
                                known_bombs += 1
                    #print(possible_bombs, number_of_bombs_local, X, Y)
                    #print()
                    
                    if (possible_bombs+known_bombs) == number_of_bombs_local:
                        if known_bombs == number_of_bombs_local:
                            pass
                        else:
                            break
            else: #these three lines are a easy way to break out of a nested loop https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
                continue
            if_break = True
            break

        #print(X, Y)

        if if_break:
            for i in [X-1, X, X+1]:
                for j in [Y-1, Y, Y+1]:
                    if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                        pass
                    elif self.visible_grid[i,j] == -2:
                        self.right_mouse_click(i,j)

        #self.clear_step()

        if np.all(np.equal(old_visible_grid.flatten(), self.visible_grid.flatten())):
            print("Not solved")
            #print(self)
            
            #possible_bombs = self.empty_grid.copy()
            possible_bombs = []
            known_number_of_bombs = []
            for X in range(self.height):
                for Y in range(self.width):
                    if self.visible_grid[X,Y] == -2:
                        for i in [X-1, X, X+1]:
                            for j in [Y-1, Y, Y+1]:
                                if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                    pass
                                elif self.visible_grid[i,j] > 0:
                                    #possible_bombs[X,Y] = 1
                                    if [X, Y] not in possible_bombs:
                                        possible_bombs.append([X, Y])
                                    if [i, j] not in known_number_of_bombs:
                                        known_number_of_bombs.append([i, j])
                        #print(possible_bombs, X, Y)
                        #print()
            #print(possible_bombs)
            #print(known_number_of_bombs)

            known_number_of_bombs_masks = self.empty_grid.copy().tolist() #tolist() because of irregular data structure
            for X, Y in known_number_of_bombs:
                known_number_of_bombs_masks[X][Y] = [[], self.visible_grid[X,Y]] #stores possible bomb locations in [0] and number of bombs needed in [1]
                tmp_mask = np.zeros((3,3)).tolist()
                for m, i in enumerate([X-1, X, X+1]):
                    for n, j in enumerate([Y-1, Y, Y+1]):
                        if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                            pass
                        elif self.visible_grid[i,j] == -4:
                            known_number_of_bombs_masks[X][Y][1] -= 1
                        elif self.visible_grid[i,j] == -2:
                            tmp_mask[m][n] = 1

                known_number_of_bombs_masks[X][Y][0] = tmp_mask

            #print(known_number_of_bombs_masks[known_number_of_bombs[0][0]][known_number_of_bombs[0][1]])

            n = 0
            solvable_pairs = []
            for X, Y in known_number_of_bombs:
                bombs_needed = known_number_of_bombs_masks[X][Y][1]
                #print(bombs_needed)


                for i in [X-1, X, X+1]:
                    for j in [Y-1, Y, Y+1]:
                        if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                            pass
                        else:
                            if [i, j] in known_number_of_bombs:
                                tmp_bombs_needed = known_number_of_bombs_masks[i][j][1]
                                #print(bombs_needed, tmp_bombs_needed, bombs_needed - tmp_bombs_needed, X, Y, i, j)
                                bomb_difference = bombs_needed - tmp_bombs_needed
                                if bomb_difference == 1:
                                    solvable_pairs.append([[X,Y],[i,j]])
                                elif bomb_difference == 2:
                                    print("difference")
                n += 1

            #print(solvable_pairs)

            bombs = []
            if len(solvable_pairs) != 0:
                for pair in solvable_pairs:
                    tmp_grid = self.empty_grid.copy()
                    X, Y = pair[0]
                    I, J = pair[1]

                    first_mask = known_number_of_bombs_masks[X][Y][0]
                    second_mask = known_number_of_bombs_masks[I][J][0]

                    #print(first_mask, second_mask)

                    #going though each mask to get ready to find where the bomb goes
                    #did this in two steps instead of loop because it's easier
                    for i in [X-1, X, X+1]:
                        for j in [Y-1, Y, Y+1]:
                            if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                pass
                            else:
                                tmp_grid[i,j] += first_mask[i-X+1][j-Y+1] #transition absolute coordinates to mask coordinates

                    for i in [I-1, I, I+1]:
                        for j in [J-1, J, J+1]:
                            if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                pass
                            else:
                                tmp_grid[i,j] += second_mask[i-I+1][j-J+1] #transition absolute coordinates to mask coordinates

                    #finding where bomb does
                    for i in [X-1, X, X+1]:
                        for j in [Y-1, Y, Y+1]:
                            if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                pass
                            else:
                                if (tmp_grid[i,j] == 1):# and (i in [I-1, I, I+1]) and (j in [J-1, J, J+1]):
                                    #print("Bomb found", i, j)
                                    bombs.append([i,j])
                                    self.right_mouse_click(i,j)
                                    

                    #print(tmp_grid)


            if len(bombs) == 0:
                print("Not solved again")
                #print(known_number_of_bombs)
                #print(known_number_of_bombs_masks)

                current_bomb_count = self.visible_grid.copy().flatten()
                current_bomb_count = np.sum([1 if x == -4 else 0 for x in current_bomb_count])
                bombs_left = self.number_of_bombs - current_bomb_count
                #print(bombs_left)

                spaces_left = len(known_number_of_bombs)
                #print(spaces_left)

                tmp_mask_grid = self.empty_grid.copy()
                tmp_placement_grid = self.empty_grid.copy()
                bomb_coordinates = []
                for X, Y in known_number_of_bombs:
                    mask = known_number_of_bombs_masks[X][Y][0]

                    tmp_placement_grid[X, Y] = 1
                    for i in [X-1, X, X+1]:
                        for j in [Y-1, Y, Y+1]:
                            if (i < 0) or (j < 0) or (i >= self.height) or (j >= self.width): #if coordinate is off of the grid
                                pass
                            else:
                                if tmp_mask_grid[i,j] != -1:
                                    tmp_mask_grid[i,j] -= mask[i-X+1][j-Y+1] #transition absolute coordinates to mask coordinates
                                    if mask[i-X+1][j-Y+1] == 1:
                                        bomb_coordinates.append([i,j])

                bomb_coordinates = np.array(bomb_coordinates)

                #print(tmp_mask_grid)
                #print(bomb_coordinates)
                #print(tmp_placement_grid)

                Y_min = bomb_coordinates[:, 0].min()
                Y_max = bomb_coordinates[:, 0].max()
                X_min = bomb_coordinates[:, 1].min()
                X_max = bomb_coordinates[:, 1].max()

                #print(tmp_mask_grid[(Y_min-1):(Y_max+2), (X_min):(X_max+2)])

                
                if Y_min == 0:
                    tmp_bomb_grid = tmp_mask_grid[(Y_min):(Y_max+2), (X_min-1):(X_max+2)]
                    tmp_numbered_grid = tmp_placement_grid[(Y_min):(Y_max+2), (X_min-1):(X_max+2)]
                    X_adjust = 1
                    Y_adjust = 0
                elif Y_max == (self.height - 1):
                    tmp_bomb_grid = tmp_mask_grid[(Y_min-1):(Y_max+2-1), (X_min-1):(X_max+2)]
                    tmp_numbered_grid = tmp_placement_grid[(Y_min-1):(Y_max+2-1), (X_min-1):(X_max+2)]
                    X_adjust = 1
                    Y_adjust = 1
                elif X_min == 0:
                    tmp_bomb_grid = tmp_mask_grid[(Y_min-1):(Y_max+2), (X_min):(X_max+2)]
                    tmp_numbered_grid = tmp_placement_grid[(Y_min-1):(Y_max+2), (X_min):(X_max+2)]
                    X_adjust = 0
                    Y_adjust = 1
                elif X_max == (self.width - 1):
                    tmp_bomb_grid = tmp_mask_grid[(Y_min-1):(Y_max+2), (X_min-1):(X_max+2-1)]
                    tmp_numbered_grid = tmp_placement_grid[(Y_min-1):(Y_max+2), (X_min-1):(X_max+2-1)]
                    X_adjust = 1
                    Y_adjust = 1
                else:
                    tmp_bomb_grid = tmp_mask_grid[(Y_min-1):(Y_max+2), (X_min-1):(X_max+2)]
                    tmp_numbered_grid = tmp_placement_grid[(Y_min-1):(Y_max+2), (X_min-1):(X_max+2)]
                    X_adjust = 1
                    Y_adjust = 1
                
                #print(tmp_bomb_grid)
                #print(tmp_numbered_grid)

                tmp_visible_grid = tmp_numbered_grid

                tmp_bomb_coordinates = []
                for i in range(tmp_bomb_grid.shape[0]):
                    for j in range(tmp_bomb_grid.shape[1]):
                        if tmp_bomb_grid[i,j] == -1:
                            tmp_bomb_coordinates.append([i, j])


                solution_found = False
                possible_bomb_permutations = permutations(tmp_bomb_coordinates, int(bombs_left))
                for permutation in possible_bomb_permutations:
                    contradiction = False
                    #print("inside loop", permutation)
                    tmp_bomb_grid_game = np.zeros(tmp_bomb_grid.shape)
                    for X, Y in permutation:
                        tmp_bomb_grid_game[X,Y] = -1

                    #print(tmp_bomb_grid_game+tmp_visible_grid)

                    for X in range(tmp_bomb_grid.shape[0]):
                        for Y in range(tmp_bomb_grid.shape[1]):
                            tmp_needed_number_of_bombs = tmp_visible_grid[X, Y]
                            tmp_actual_number_of_bombs = 0
                            for i in [X-1, X, X+1]:
                                for j in [Y-1, Y, Y+1]:
                                    if (i < 0) or (j < 0) or (i >= tmp_bomb_grid.shape[0]) or (j >= tmp_bomb_grid.shape[1]): #if coordinate is off of the grid
                                        pass
                                    else:
                                        if (tmp_bomb_grid_game[i,j] == -1) and (tmp_visible_grid[X,Y] == 1):
                                            tmp_actual_number_of_bombs += 1
                            #print(tmp_needed_number_of_bombs, tmp_actual_number_of_bombs, 'needed and actual')
                            if tmp_needed_number_of_bombs != tmp_actual_number_of_bombs:
                                contradiction = True
                                break

                    if not contradiction:
                        solution_found = True
                        break

                solving_permutation = np.array(permutation)
                solving_permutation[:,0] += Y_min - Y_adjust
                solving_permutation[:,1] += X_min - X_adjust
                #print(solving_permutation)

                for X, Y in solving_permutation:
                    self.right_mouse_click(X, Y)

        self.clear_step()
        #print(self.done, self.win)


thing = Solving_Game(10, 10, 20, True)
print(thing.combined_grid)

thing.left_mouse_click(0,9)
thing.solve_step()
thing.left_mouse_click(9,0)
thing.solve_step()
thing.left_mouse_click(4,4)
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
thing.solve_step()
print(thing)


'''
thing = Game(7, 7, 10, False)
thing.left_mouse_click(1,1)
thing.left_mouse_click(4,4)
thing.left_mouse_click(1,6)
thing.left_mouse_click(0,3)
thing.left_mouse_click(1,2)
thing.right_mouse_click(0,2)
thing.right_mouse_click(0,1)
thing.right_mouse_click(5,4)
thing.right_mouse_click(5,3)
thing.left_mouse_click(6,4)
thing.left_mouse_click(6,3)
thing.left_mouse_click(6,2)
thing.left_mouse_click(5,2)
thing.left_mouse_click(5,1)
thing.right_mouse_click(6,1)
thing.left_mouse_click(3,0)
thing.left_mouse_click(0,0)
thing.right_mouse_click(2,0)
thing.right_mouse_click(1,0)
thing.left_mouse_click(4,0)
thing.right_mouse_click(5,0)
thing.right_mouse_click(6,0)
print(thing)
'''
