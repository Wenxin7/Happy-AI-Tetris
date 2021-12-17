# This file would be imported in AI game level
import random
import pygame
from numpy import *
import player


def judging_centers(done_area, block_shape):
    '''
    This function will enumerate all possible position and rotation type of blocks which are randomly
    created, score which posibility and find the optimal possibilites. Finally we could get the best 
    rotation type and optimal position to put the block.

    **Parameters**

        done_area: *list*
            the coordinates of the blocks which are already placed in board
        block_shape: *list*
            the list which contain 1-4 kinds of rotation type, each type owns 4 coordinates of 
            cubes in a kind of block

    **Output**

        the type of the block, the rotation type, the optimal position and the start point of block

    '''
    block_dir = {
        'I': [[(0, -4), (0, -3), (0, -2), (0, -1)],
              [(-1, -3), (0, -3), (1, -3), (2, -3)]],
        'J': [[(0, -5), (0, -4), (0, -3), (-1, -3)],
              [(2, -3), (1, -3), (0, -3), (0, -4)],
              [(0, -1), (0, -2), (0, -3), (1, -3)],
              [(-2, -3), (-1, -3), (0, -3), (0, -2)]],
        'L': [[(0, -5), (0, -4), (0, -3), (1, -3)],
              [(2, -3), (1, -3), (0, -3), (0, -2)],
              [(0, -1), (0, -2), (0, -3), (-1, -3)],
              [(-2, -3), (-1, -3), (0, -3), (0, -4)]],
        'O': [[(-1, -4), (-1, -3), (0, -4), (0, -3)]],
        'S': [[(1, -4), (0, -4), (0, -3), (-1, -3)],
              [(1, -2), (1, -3), (0, -3), (0, -4)]],
        'T': [[(-1, -3), (0, -3), (1, -3), (0, -4)],
              [(0, -4), (0, -3), (1, -3), (0, -2)],
              [(-1, -3), (0, -3), (1, -3), (0, -2)],
              [(0, -4), (0, -3), (-1, -3), (0, -2)]],
        'Z': [[(-1, -4), (0, -4), (0, -3), (1, -3)],
              [(0, -4), (0, -3), (-1, -3), (-1, -2)]]
    }

    def block_to_matrix():
        '''
        This function aims to create a matrix used as boundary condition

        **Output**
            the matrix with 25 lists and 10 'None' in each list to simulation coordinates
        '''
        screen_matrix = [[None] * columns for i in range(rows)]
        for done in done_area:
            screen_matrix[done[1]+2][done[0]+4] = 0
        return screen_matrix

    screen_matrix = block_to_matrix()

    def wrong_position(block_type, block_id, fall_position):
        '''
        Judge if the input block type, its rotation type and predicted fallen sites are valid

        **Parameters**

            block_type: *string*
                the type of a block, in alphabet
            block_id: *int*
                the index of rotation type
            fall_position: *tuple*
                delta x and delta y, which is the difference of final position and start point

        **Output**
            validity of the fallen position
        '''

        all_block_position = [(cube[0] + fall_position[0], cube[1] + fall_position[1])
                              for cube in block_dir[block_type][block_id]]
        for cube_co in all_block_position:
            if cube_co[0] < -4:
                return True
            if cube_co[1] < -2:
                return True
            if cube_co[0] > 5:
                return True
            if cube_co[1] > 22:
                return True
            if screen_matrix[cube_co[1]+2][cube_co[0]+4] != None:
                return True
        return False

    # get all possible positions to all the given blocks and enumerate them
    given_block_type = 'S'
    for b_t in block_dir.keys():
        if block_shape == block_dir[b_t]:
            given_block_type = b_t

    centerList = []
    for rotation_type in range(len(block_shape)):
        for w in range(-4, 6):
            for h in range(25, 0, -1):
                if (wrong_position(given_block_type, rotation_type, (w, h)) == False) and \
                        (wrong_position(given_block_type, rotation_type, (w, h+1)) == True):

                    centerList.append(
                        [given_block_type, rotation_type, (w, h)])

    # delete the invalid possibilities

    for c_l in centerList[:]:
        dx = int(c_l[2][0])
        dy = int(c_l[2][1])

        new_cor = [(cube[0] + dx, cube[1] + dy)
                   for cube in block_dir[c_l[0]][c_l[1]]]

        for cor in new_cor:
            for i in range(-2, cor[1]):
                if screen_matrix[i+2][cor[0]+4] == 0:
                    if c_l in centerList:
                        centerList.remove(c_l)

    # count scores parts, find the optimal case of ratation type and falling position
    for centerlist in centerList:

        # get LandingHeight, and add it to the 4th column of centerlist
        h_list = []
        for cor in block_dir[centerlist[0]][centerlist[1]]:
            h_list.append(cor[1] + centerlist[2][1])
        LandingHeight = 23 - min(h_list)
        centerlist.append(LandingHeight)

        # get the matrix after the choosen block fallen (in one case)
        matrix_after = [[None] * columns for i in range(rows)]
        for done in done_area:
            matrix_after[done[1]+2][done[0]+4] = 0
        for new_cor in block_dir[centerlist[0]][centerlist[1]]:
            n_x = new_cor[0] + centerlist[2][0]
            n_y = new_cor[1] + centerlist[2][1]
            matrix_after[n_y+2][n_x+4] = 0

        # get eliminate contribution, the line number which could be eliminate after fallen times
        # the block in the eliminate line, and add it to the 5th column of centerlist

        new_block_position = []
        for cube_pos in block_dir[centerlist[0]][centerlist[1]]:
            new_block_position.append(
                (cube_pos[0]+centerlist[2][0], cube_pos[1]+centerlist[2][1]))

        eliminate_line = 0
        useful_cube = 0
        elimination_contribution = 0
        for i in range(rows-1, 0, -1):
            t = 0
            for j in range(columns):
                if matrix_after[i][j] is not None:
                    t += 1
            if t == columns:
                eliminate_line += 1
                for b_posi in new_block_position:
                    if b_posi[1] == i-2:
                        useful_cube += 1

        elimination_contribution = eliminate_line * useful_cube
        centerlist.append(elimination_contribution)

        # get BroadRollTrandition, and add it to the 6th column of centerlist
        roll_transition_times = 0
        for i in range(rows-1, 0, -1):
            for j in range(columns-1):
                if (matrix_after[i][j] == None and matrix_after[i][j + 1] != None) or (matrix_after[i][j] != None and matrix_after[i][j + 1] == None):
                    roll_transition_times += 1
        centerlist.append(roll_transition_times)

        # get BroadColTrandition, and add it to the 7th column of centerlist
        col_transition_times = 0
        for j in range(columns):
            for i in range(rows-1, 1, -1):
                if (matrix_after[i][j] == None and matrix_after[i-1][j] != None) or (matrix_after[i][j] != None and matrix_after[i-1][j] == None):
                    col_transition_times += 1
        centerlist.append(col_transition_times)

        # get empty_holes, and add it to the 8th column of centerlist
        empty_holes = 0
        for j in range(columns):
            t = None
            for i in range(rows):
                if matrix_after[i][j] != None and t == None:
                    t = 0
                if matrix_after[i][j] == None and t != None:
                    t += 1
            if t != None:
                empty_holes += t
        centerlist.append(empty_holes)

        # get wells_number, and add it to the 9th column of centerlist
        wells_number = 0
        wall_brick = 0
        for i in range(columns):
            for j in range(rows):
                if matrix_after[j][i] == None:
                    if (i == 0) and (matrix_after[j][i+1] != None):
                        wall_brick += 1
                    elif (i > 0) and (i < columns-1) and (matrix_after[j][i-1] != None) and (matrix_after[j][i+1] != None):
                        wall_brick += 1
                    elif (i == columns-1) and (matrix_after[j][i-1] != None):
                        wall_brick += 1
                else:
                    wells_number += ((wall_brick + 1)*wall_brick/2)
                    wall_brick = 0
        centerlist.append(wells_number)

        # get whole point of each center position of a kind rotation, and add it to the 10th column of centerlist
        whole_point = -45*centerlist[3] + 34*centerlist[4] - 32 * \
            centerlist[5] - 98*centerlist[6] - \
            79*centerlist[7] - 34*centerlist[8]

        centerlist.append(whole_point)

    # choose the optimal block with rotation and center, the one with highest scores
    largest_point_block = centerList[0]
    for centerlist in centerList:
        if centerlist[9] >= largest_point_block[9]:
            largest_point_block = centerlist

    # return the type of blocks, rotation type, (dlt_x, dlt_y) to move, and start point of the block
    return largest_point_block[0], largest_point_block[1], largest_point_block[2], block_dir[largest_point_block[0]][largest_point_block[1]]


# Define block shapes and shapes after rotation
T = [[(-1, -3), (0, -3), (1, -3), (0, -4)],
     [(0, -4), (0, -3), (1, -3), (0, -2)],
     [(-1, -3), (0, -3), (1, -3), (0, -2)],
     [(0, -4), (0, -3), (-1, -3), (0, -2)]]
Z = [[(-1, -4), (0, -4), (0, -3), (1, -3)],
     [(0, -4), (0, -3), (-1, -3), (-1, -2)]]
S = [[(1, -4), (0, -4), (0, -3), (-1, -3)],
     [(1, -2), (1, -3), (0, -3), (0, -4)]]
I = [[(0, -4), (0, -3), (0, -2), (0, -1)],
     [(-1, -3), (0, -3), (1, -3), (2, -3)]]
L = [[(0, -5), (0, -4), (0, -3), (1, -3)],
     [(2, -3), (1, -3), (0, -3), (0, -2)],
     [(0, -1), (0, -2), (0, -3), (-1, -3)],
     [(-2, -3), (-1, -3), (0, -3), (0, -4)]]
J = [[(0, -5), (0, -4), (0, -3), (-1, -3)],
     [(2, -3), (1, -3), (0, -3), (0, -4)],
     [(0, -1), (0, -2), (0, -3), (1, -3)],
     [(-2, -3), (-1, -3), (0, -3), (0, -2)]]
O = [[(-1, -4), (-1, -3), (0, -4), (0, -3)]]

blocks = [T, Z, S, I, L, J, O]

# Define the color
colors = [(174, 99, 120), (19, 131, 194), (253, 143, 82),
          (148, 180, 71), (185, 194, 227), (196, 128, 98), (240, 166, 179)]

# Define the game board
# The size of small square is 25 x 25
cell_size = 25
# The game board has 10 columns
columns = 10
# The game board has 25 rows
rows = 25
# The line draw on the screen is 1 mm thick
line = 1
# The size of game board
board_width = columns * (cell_size + line) + line
board_height = rows * (cell_size + line) + line
# The size of the whole screen window
screen_width = 500
screen_height = 800
# The coordinate of the game board on the screen
board_start_x = (screen_width - board_width) // 2
board_start_y = screen_height - board_height
fps = 60


def game_text(screen, font, x, y, text, color):
    text = font.render(text, 1, color)
    screen.blit(text, (x, y))


def display_screen(screen):
    '''
    This function is to setting all the elements that will show on the home page and
    draw the background.

    **Parameters**

        screen: *object*
            the out put of pygame window

    **Output**

       All the texts that will be shown on the screen
    '''

    screen.fill((252, 230, 201))
    pygame.draw.rect(screen, (255, 250, 250), pygame.Rect(
        50, 100, board_width, board_height))
    for x in range(columns + 1):
        pygame.draw.line(screen, (0, 0, 0), (50 + x * (cell_size + line),
                         100), (50 + x * (cell_size + line), board_height + 99))
    for y in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (50, y * (cell_size + line) + 100),
                         (board_width + 49, y * (cell_size + line) + 100))
    pygame.font.init()
    font1 = pygame.font.SysFont('arial', 60)
    font2 = pygame.font.SysFont('arial', 72)  # bigger font for "GAME OVER"
    font_2 = pygame.font.SysFont('Arial', 20)
    bg_cor1 = (50 + 11 * (cell_size + line), 100)
    bg_width = 5 * (cell_size + line) + line
    bg_height = 2 * (cell_size + line) + line
    font_width = int(font_2.size("Next Block")[0])
    font_height = int(font_2.size("Next Block")[1])
    font_x = bg_cor1[0] + (bg_width - font_width) / 2
    font_y = bg_cor1[1] + (bg_height - font_height) / 2
    game_text(screen, font_2, font_x, font_y +
              20, "Next Block", (104, 149, 191))


def creat_block():
    '''
    This function is for creating new blocks

    **Parameters**
        None

    **Output**

        block: *list*
            each coordinate of four grids in this block
        block_shape: *list*
            the shape name of the block. eg. T, O, L, S
            the letter variable is the list which includes all coordinates of the
            initial shapes and shapes after rotation.
        block_id: *int*
            the index of newly created block in the corresponding block list.
    '''
    # Random choice from all kinds of block shape list
    block_shape = random.choice(blocks)
    # The newly created block's initial direction will always be the first one in the corresponding block list
    block = block_shape[0]
    # Store the index as block_id for further rotation function
    block_id = block_shape.index(block)
    return block, block_shape, block_id


class Blocks(object):
    '''
    This class create a wrapper for functions which implement all the operations for tetris blocks,
    including movement, rotation, create new block after landing and eliminating rows when a row is full.
    Also, it has some checking functions to check whether some certain operation can be done or not.
    The functions of drawing blocks are also included.

    **Parameters**

        list and int: *block* and *block_shape* and *block_id*
            Each coordinate of four grids in this block. The letter variable is the
            list which includes all coordinates of the initial shapes and shapes after rotation.
            The index of newly created block in the corresponding block list.
    '''
    def __init__(self, block, block_shape,  block_id):
        # The color of each block will be chosen by random choice from color list.
        self.color_ind = random.choice(len(colors))
        self.color = colors[self.color_ind]
        self.block_shape = block_shape
        self.block = block
        # The initial index of every new-born block
        self.block_id = block_id

    def __call__(self):
        return self.block

    def chk_move(self, del_x, del_y):
        '''
        This function is for checking whether the current block landed on the bottom
        of the board or out of the x range of the board. To check the block can continue to move or not.

        **Parameters**

            del_x: *int*
                The move step of the block in x direction.
            del_y: *int*
                The move step of the block in y direction.

        **Output**

           valid: *bool*
                Whether the movement are valid (True) or not (False).
        '''
        for sq in self.block:
            if sq[1] + del_y > 22 or sq[0] + del_x < -4 or sq[0] + del_x > 5:
                return False
        return True

    def chk_overlap(self, del_x, del_y):
        '''
        This function is for checking whether the current block will overlap with landed blocks or not.

        **Parameters**

            del_x: *int*
                The move step of the block in x direction.
            del_y: *int*
                The move step of the block in y direction.

        **Output**

           valid: *bool*
                Whether the overlap are True or not (False).
        '''
        for sq in self.block:
            if (sq[0] + del_x, sq[1] + del_y) in self.done_area:
                return False
        return True

    def chk_over(self):
        '''
        This function is for checking whether the current block has reach the top of the board or not.

        **Parameters**

            del_x: *int*
                The move step of the block in x direction.
            del_y: *int*
                The move step of the block in y direction.

        **Output**

           valid: *bool*
                Whether the overlap are True or not (False).
        '''
        # check whether there are done blocks already in the top row
        for sq in self.block:
            if sq[1] <= -2:
                return False
        return True

    def move(self, del_x, del_y):
        '''
        This function is to implement the movement of the blocks.

        **Parameters**

            del_x: *int*
                The move step of the block in x direction.
            del_y: *int*
                The move step of the block in y direction.

        **Output**

           block: *list*
                The block after certain movement.
        '''

        new_block = []
        for pos in self.block:
            new_x = pos[0] + del_x
            new_y = pos[1] + del_y
            new_block.append((new_x, new_y))
            self.block = new_block
        return self.block

    done_area = []  # fallen blocks
    cur_block = None  # falling block
    ex_color = []
    whole_cor = []

    def create_next(self):
        '''
        This function is for creating a next block when current block is falling. The next block will
        be shown as a preview.

        **Parameters**
            None

        **Output**

            next_block: *list*
                each coordinate of four grids in newly created block
            next_shape: *list*
                the shape name of the newly created block. eg. T, O, L, S
            next_block_id: *int*
                the index of newly created block in the corresponding block list.
            next_color: *tuple*
                the color of newly created block
        '''
        N_block = creat_block()
        next_block = N_block[0]
        next_shape = N_block[1]
        self.next_block = next_block
        self.next_shape = next_shape
        # get the initial index of every new blocks for further block rotation function
        self.next_block_id = self.next_shape.index(self.next_block)
        new_color_ind = random.choice(len(colors))
        new_color = colors[new_color_ind]
        self.next_color = new_color
        return self.next_block, self.next_shape, self.next_block_id, self.next_color

    def draw_next(self, screen):
        '''
        This function is to draw the next block on the upper right side of the game screen as preview.

        **Parameters**

            screen: *object*
                the out put of pygame screen window

        **Output**

           The preview of next block with certain color that will be shown on the screen
        '''
        # Calculate the position of white rectangle background of the next block preview part
        bg_cor1 = (50 + 11 * (cell_size + line), 175)
        # Calculate the size of white rectangle background of the next block preview part
        
        bg_width = 5 * (cell_size + line) + line
        bg_height = 7 * (cell_size + line) + line
        # Draw the white rectangle background on the upper right side of the game screen
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
            bg_cor1[0], bg_cor1[1], bg_width, bg_height))
        for sq in self.next_block:
            # Draw the lines of the block

            line_corn1 = (50 + (sq[0] + 13) * (cell_size + line),
                          100 + (sq[1] + 9) * (cell_size + line))
            line_corn2 = (50 + (sq[0] + 14) * (cell_size + line),
                          100 + (sq[1] + 9) * (cell_size + line))
            line_corn3 = (50 + (sq[0] + 14) * (cell_size + line),
                          100 + (sq[1] + 10) * (cell_size + line))
            line_corn4 = (50 + (sq[0] + 13) * (cell_size + line),
                          100 + (sq[1] + 10) * (cell_size + line))
            corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
            # Fill all the square grids with corresponding color
            
            pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
            pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
            pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
            pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
            pygame.draw.rect(screen, self.next_color, pygame.Rect(
                corn1[0], corn1[1], cell_size, cell_size))

    def creat_new_block(self):
        '''
        This function is for creating new block after last block land. In this game, The block created by
        create_next() function will be passed to the showing block.

        **Parameters**
            None

        **Output**

            block: *list*
                each coordinate of four grids in the coming block
            shape: *list*
                the shape name of the coming block. eg. T, O, L, S
            color: *tuple*
                the color of the coming block
        '''
        new_block = self.next_shape
        d_x = judging_centers(self.done_area, new_block)[2][0]
        block_cor = judging_centers(self.done_area, new_block)[3]
        new_cor = []
        for co in block_cor:

            n_x = co[0] + d_x
            n_y = co[1]
            new_cor.append((n_x, n_y))
        self.block = new_cor
        self.block_shape = new_cor
        self.color = self.next_color
        self.create_next()
        return self.block, self.color, self.block_shape

    def falling(self):
        '''
        This function is to implement the falling of blocks.

        **Parameters**
            None

        **Output**

            game: *int*
                It returns two numbers,1 and 2. 1 means the game is still running, while the 2 means the
                game is over.
        '''
        if self.chk_move(0, 1):
            # Check whether the block has landed or not

            if self.chk_overlap(0, 1):
                # Check whether the block will over lap with landed block or not
                # Move 1 step in y direction once.
                self.move(0, 1)
            else:
                '''
                First, check whether the current block will overlap with the block below 
                If the block overlap with the block below, and this block is already out of the game board area,
                the game will stop.
                '''
                if self.chk_over():
                    '''
                    If the current block won't be out of the top range, then the block will landed on
                    the previous block.
                    '''
                    for bol in self.block:
                        # Store the block position and corresponding color in to done_area and ex_color list.

                        self.ex_color.append(self.color)
                        self.done_area.append(bol)
                    # Check whether need to remove a full row after the block landed.
                    
                    self.clear_row()
                    # After landing, show the new block.

                    self.creat_new_block()
                else:
                    for bol in self.block:
                        # Add the last block to done_area list
                        self.ex_color.append(self.color)
                        self.done_area.append(bol)
        else:
            '''
            If the current block has already landed on the bottom of the board, then the block and it's color
            will be stored in corresponding lists.
            '''
            for bol in self.block:
                self.ex_color.append(self.color)
                self.done_area.append(bol)
            # Check whether need to remove a full row after the block landed.
            
            self.clear_row()
            # After landing, show the new block.

            self.creat_new_block()

    def key_control(self, del_x, del_y):
        '''
        This function is to implement the movement in left or right direction of the blocks.

        **Parameters**

            del_x: *int*
                The move step of the block in x direction.
            del_y: *int*
                The move step of the block in y direction.

        **Output**

           The operation of the block.
        '''
        if self.chk_move(del_x, del_y):
            # Check whether the block has landed or not

            if self.chk_overlap(del_x, del_y):
                # Check whether the block will overlap with landed block or not
                # Then move the block by certain step
                self.move(del_x, del_y)

    def chk_clear(self, list1, list2):
        for i in list1:
            if i not in list2:
                return False
        return True

    clear_num = 0

    def clear_row(self):
        for y in range(-2, 23):
            row = []
            for x in range(-4, 6):
                row.append((x, y))
            # generate all the coordinate of points into the whole coordinate list
            self.whole_cor.append(row)
            # To make sure each row in this list is arranged from bottom to top
            self.whole_cor.reverse()
        for row in self.whole_cor:
            if self.chk_clear(row, self.done_area):
                # record the row number of the row that will be cleared.
                row_done = row[0][1]
                for i in row:
                    self.ex_color.pop(self.done_area.index(i))
                    self.done_area.remove(i)
                self.clear_num += 1
                done_temp = []
                for bl in self.done_area[:]:
                    if bl[1] < row_done:
                        done_temp.append((bl[0], bl[1] + 1))
                        self.done_area.remove(bl)
                for i in done_temp:
                    self.done_area.append(i)

    def draw_score(self, screen):
        bg_cor1 = (50 + 11 * (cell_size + line), 400)
        bg_width = 5 * (cell_size + line) + line
        bg_height = 2 * (cell_size + line) + line
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
            bg_cor1[0], bg_cor1[1] + 55, bg_width, bg_height))
        font_2 = pygame.font.SysFont('Arial', 20)
        font_3 = pygame.font.SysFont('Cambria Math', 24)
        font_width = int(font_2.size("Score")[0])
        font_height = int(font_2.size("Score")[1])
        font_x = bg_cor1[0] + (bg_width - font_width) / 2
        font_y = bg_cor1[1] + 30
        font_width_s = int(font_3.size('Score: %d' %
                           (self.clear_num * 100))[0])
        font_height_s = int(font_3.size('Score: %d' %
                            (self.clear_num * 100))[1])
        font_x_s = bg_cor1[0] + (bg_width - font_width_s) / 2
        font_y_s = font_y + font_height_s + 25
        game_text(screen, font_2, font_x, font_y, "Score", (104, 149, 191))
        game_text(screen, font_3, font_x_s, font_y_s + 2, 'Score: %d' %
                  (self.clear_num * 100), (178, 34, 34))

    def draw_block(self, cell_size, line, screen):
        if self.falling:
            for sq in self.block:
                line_corn1 = (
                    50 + (sq[0] + 4) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                line_corn2 = (
                    50 + (sq[0] + 5) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                line_corn3 = (
                    50 + (sq[0] + 5) * (cell_size + line), 100 + (sq[1] + 3) * (cell_size + line))
                line_corn4 = (
                    50 + (sq[0] + 4) * (cell_size + line), 100 + (sq[1] + 3) * (cell_size + line))
                corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
                pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
                pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
                pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
                pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
                pygame.draw.rect(screen, self.color, pygame.Rect(
                    corn1[0], corn1[1], cell_size, cell_size))
            for pot in self.done_area:
                line_corn1 = (
                    50 + (pot[0] + 4) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                line_corn2 = (
                    50 + (pot[0] + 5) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                line_corn3 = (
                    50 + (pot[0] + 5) * (cell_size + line), 100 + (pot[1] + 3) * (cell_size + line))
                line_corn4 = (
                    50 + (pot[0] + 4) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
                pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
                pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
                pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
                pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
                pygame.draw.rect(screen, self.ex_color[self.done_area.index(
                    pot)], pygame.Rect(corn1[0], corn1[1], cell_size, cell_size))


def main():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    Block = creat_block()
    block = Block[0]
    block_shape = Block[1]
    block_id = Block[2]
    screen_block = Blocks(block, block_shape, block_id)
    screen_block.create_next()
    screen_block.done_area = []
    screen_block.ex_color = []
    font_level_small = pygame.font.SysFont('Arial', 25)
    font_level_large = pygame.font.SysFont('Arial', 30)
    w = int(font_level_small.size("return")[0])
    h = int(font_level_small.size("return")[1])
    x = 75 + 11 * (cell_size + line)
    y = 675
    move_time = 30
    time = pygame.time.get_ticks() + move_time
    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x < mouse[0] < x + w and y < mouse[1] < y + h:
                    player.Home_page()
        display_screen(screen)
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            game_text(screen, font_level_large, x, y, "return", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x, y, "return", (90, 167, 167))
        screen_block.draw_score(screen)
        screen_block.draw_block(cell_size, line, screen)
        screen_block.draw_next(screen)
        pygame.display.update()
        if pygame.time.get_ticks() >= time:
            time += move_time
            screen_block.falling()
