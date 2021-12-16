import random
import pygame
from numpy import *
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_RETURN, MOUSEBUTTONDOWN
import tetris_ai_optimize

# Define the coordination of different block shapes and shapes after rotation
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
# The reward block is for the game reward
reward = [[(0, -3)]]
# Shape name of the block
blocks = [T, Z, S, I, L, J, O]

# Define the color
colors = [(174, 99, 120), (19, 131, 194), (253, 143, 82), (148, 180, 71), (185, 194, 227), (196, 128, 98), (240, 166, 179)]

# Define all the parameters of the game board
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


def game_text(screen, font, x, y, message, color):
    '''
    This function is for displaying the text on the window screen in certain font, position and color

    **Parameters**

        screen: *object*
            the out put of pygame window
        font: *object*
            the font style and size of the text
        x: *int*
            x coordination of the text position
        y: *int*
            y coordination of the text position
        message: *string*
            the content of the text that will show on the screen
        color: *tuple*
            the color of the text
    **Output**

        The text will show on the screen
    '''
    text = font.render(message, 1, color)
    screen.blit(text, (x, y))


def home_display(screen):
    '''
    This function is to setting all the elements that will show on the home page and
    draw the background.

    **Parameters**

        screen: *object*
            the out put of pygame window

    **Output**

       All the texts that will be shown on the screen
    '''
    # The colour of the home page background
    screen.fill((252, 230, 201))
    # Set the font style and size of the game title
    font_title = pygame.font.SysFont('Arial', 60)
    # Get the size of the title for calculating the location coordinate
    font_title_x = int(font_title.size("Happy AI Tetris")[0])
    font_title_y = int(font_title.size("Happy AI Tetris")[1])
    # The title will show in the middle of the width of the screen.
    x = (screen_width - font_title_x)/2
    y = 75
    game_text(screen, font_title, x, y, "Happy AI Tetris", (19, 131, 194))


def button_home(screen, text, level, func):
    '''
    This function is to create buttons used in the home page. By clicking the certain button, the
    screen will jump to the corresponding game level.

    **Parameters**
        screen: *object*
            the out put of pygame window
        text: *string*
            the content shown on the button
        level: *int*
            the number used to control the y distance of different level button
        func: *function*
            the function that will be executed by clicking the button, and it will
            run the corresponding game level

    **Output**

        the buttons will be shown and worked on the home page screen
    '''
    # Use pygame.mouse module get the position of mouse
    # mouse = pygame.mouse.get_pos()
    # # Set the font style of normal button text
    # font_level_small = pygame.font.SysFont('Arial', 30)
    # # Set the font style of the button text when mouse is within the button area
    # # The font is bigger than normal state when mouse pointing to the button
    # font_level_large = pygame.font.SysFont('Arial', 35)
    # # Do the calculation for locating the button
    # w = int(font_level_small.size(text)[0])
    # h = int(font_level_small.size(text)[1])
    # x = (screen_width - w)/2
    # y = 200 + 100 * level
    '''
    When mouse is not pointing to the button, the button shows in smaller font and in light blue.
    When mouse is pointing to the button, the button will be larger and become dark blue
    '''
    # if x < mouse[0] < x + w and y < mouse[1] < y + h:
    #     # larger and dark blue button
    #     game_text(screen, font_level_large, x, y, text, (56, 82, 132))
    #     '''
    #     Using get_pressed module to get the state of mouse left button. When player click the button,
    #     this function will return a True value to execute the game function.
    #     '''
    #
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         func()
    # else:
    # larger and dark blue button
    # smaller and light blue button
    #     game_text(screen, font_level_small, x, y, text, (90, 167, 167))


def button_return(screen, text, x, y, func):
    '''
    This function is to create a "return" button used in each level game page. By clicking the "return" button, the
    screen will jump back to the home page.

    **Parameters**
        screen: *object*
            the out put of pygame window
        text: *string*
            the content shown on the button
        x: *int*
            the x coordinate of the button position
        y: *int*
            the y coordinate of the button position
        func: *function*
            the function that will be executed by clicking the button, and it will
            run the home page function

    **Output**

        the buttons will be shown and worked on each level game page
    '''
    # # Use pygame.mouse module get the position of mouse
    # mouse1 = pygame.mouse.get_pos()
    # font_level_small = pygame.font.SysFont('Arial', 25)
    # font_level_large = pygame.font.SysFont('Arial', 30)
    # w = int(font_level_small.size(text)[0])
    # h = int(font_level_small.size(text)[1])
    # if x < mouse1[0] < x + w and y < mouse1[1] < y + h:
    #     # larger and dark blue button
    #     game_text(screen, font_level_large, x, y, text, (56, 82, 132))
    #     '''
    #     Using get_pressed module to get the state of mouse left button. When player click the button,
    #     this function will return a True value to execute the home page function.
    #     '''
    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 func()
    #
    # else:
    #     # smaller and light blue button
    #     if x < mouse1[0] < x + w and y < mouse1[1] < y + h:
    #         game_text(screen, font_level_large, x, y, text, (56, 82, 132))
    #         game_text(screen, font_level_small, x, y, text, (90, 167, 167))


def Home_page():
    '''
    This function is for displaying home page of the game window

    **Parameters**
        None

    **Output**

        All the texts, buttons and background are shown on the screen
    '''
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    # Set the font style of normal button text
    font_level_small = pygame.font.SysFont('Arial', 30)
    # Set the font style of the button text when mouse is within the button area
    # The font is bigger than normal state when mouse pointing to the button
    font_level_large = pygame.font.SysFont('Arial', 35)
    # Do the calculation of the size and location of all the buttons
    w_1 = int(font_level_small.size("Level 1")[0])
    h_1 = int(font_level_small.size("Level 1")[1])
    x_1 = (screen_width - w_1) / 2
    y_1 = 200 + 100 * 1
    w_2 = int(font_level_small.size("Level 2")[0])
    h_2 = int(font_level_small.size("Level 2")[1])
    x_2 = (screen_width - w_2) / 2
    y_2 = 200 + 100 * 2
    w_3 = int(font_level_small.size("Level 3")[0])
    h_3 = int(font_level_small.size("Level 3")[1])
    x_3 = (screen_width - w_3) / 2
    y_3 = 200 + 100 * 3
    w_ai = int(font_level_small.size("AI Tetris")[0])
    h_ai = int(font_level_small.size("AI Tetris")[1])
    x_ai = (screen_width - w_ai) / 2
    y_ai = 200 + 100 * 4
    w_q = int(font_level_small.size("Quit")[0])
    h_q = int(font_level_small.size("Quit")[1])
    x_q = (screen_width - w_q) / 2
    y_q = 200 + 100 * 5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Use pygame.mouse module get the position of mouse
            mouse = pygame.mouse.get_pos()
            '''
            For this event, it is basically creating a "return" button used in each level game page. 
            By clicking the "return" button, the screen will jump back to the home page.
            '''
            # When the mouse button is "down" and in specific button area,
            # the corresponding level game will be launched.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # "Level 1" area
                if x_1 < mouse[0] < x_1 + w_1 and y_1 < mouse[1] < y_1 + h_1:
                    level_1()
                # "Level 2" area
                if x_2 < mouse[0] < x_2 + w_2 and y_2 < mouse[1] < y_2 + h_2:
                    level_2()
                # "Level 3" area
                if x_3 < mouse[0] < x_3 + w_3 and y_3 < mouse[1] < y_3 + h_3:
                    level_3()
                # "AI Tetris" area
                if x_ai < mouse[0] < x_ai + w_ai and y_ai < mouse[1] < y_ai + h_ai:
                    tetris_ai_optimize.main()
                # "Quit" area
                if x_q < mouse[0] < x_q + w_q and y_q < mouse[1] < y_q + h_q:
                    quit_game()
        # Let all the elements added by home_display() function show on screen
        home_display(screen)
        mouse = pygame.mouse.get_pos()
        '''
        After getting the mouse position at every moment, When mouse is not pointing to the button, 
        the button shows in smaller font and in light blue. When mouse is pointing to the button, 
        the button will be larger and become dark blue.
        '''
        if x_1 < mouse[0] < x_1 + w_1 and y_1 < mouse[1] < y_1 + h_1:
            # larger and dark blue button
            game_text(screen, font_level_large, x_1, y_1, "Level 1", (56, 82, 132))
        else:
            # smaller and light blue button
            game_text(screen, font_level_small, x_1, y_1, "Level 1", (90, 167, 167))
        if x_2 < mouse[0] < x_2 + w_2 and y_2 < mouse[1] < y_2 + h_2:
            # Same with the "Level 1" button
            game_text(screen, font_level_large, x_2, y_2, "Level 2", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x_2, y_2, "Level 2", (90, 167, 167))
        if x_3 < mouse[0] < x_3 + w_3 and y_3 < mouse[1] < y_3 + h_3:
            game_text(screen, font_level_large, x_3, y_3, "Level 3", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x_3, y_3, "Level 3", (90, 167, 167))
        if x_ai < mouse[0] < x_ai + w_ai and y_ai < mouse[1] < y_ai + h_ai:
            game_text(screen, font_level_large, x_ai, y_ai, "AI Tetris", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x_ai, y_ai, "AI Tetris", (90, 167, 167))
        if x_q < mouse[0] < x_q + w_q and y_q < mouse[1] < y_q + h_q:
            game_text(screen, font_level_large, x_q, y_q, "Quit", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x_q, y_q, "Quit", (90, 167, 167))
        pygame.display.update()


def quit_game():
    '''
    This function is to execute quiting the game window

    **Parameters**
        None

    **Output**

        Quiting the window
    '''
    pygame.quit()
    quit()


def display_screen(screen):
    '''
    This function is to setting all the elements that will show on the game playing page and
    draw the background.

    **Parameters**

        screen: *object*
            the out put of pygame window

    **Output**

       All the texts and graphics that will be shown on the screen
    '''
    # Fill the background with a single color
    screen.fill((252, 230, 201))
    # Draw the background of playing area board
    pygame.draw.rect(screen, (255, 250, 250), pygame.Rect(50, 100, board_width, board_height))
    # Draw all the column and row lines to generate grid board for playing tetris
    for x in range(columns + 1):
        pygame.draw.line(screen, (0, 0, 0), (50 + x * (cell_size + line), 100), (50 + x * (cell_size + line), board_height + 99))
    for y in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (50, y * (cell_size + line) + 100), (board_width + 49, y * (cell_size + line) + 100))
    # Adding pause hint on the left side of the screen
    pygame.font.init()
    font_1 = pygame.font.SysFont('Arial', 12)
    font_width = int(font_1.size("Press SPACE to pause the game")[0])
    font_height = int(font_1.size("Press SPACE to pause the game")[1])
    game_text(screen, font_1, 318, 600, "Press SPACE to pause the game", (226, 90, 83))
    '''
    bg_cor1 means the background upper left corner of the "Next block" rectangle which is used to show 
    the coming block
    '''
    bg_cor1 = (50 + 11 * (cell_size + line), 100)
    # The size of the "Next block" rectangle
    bg_width = 5 * (cell_size + line) + line
    bg_height = 2 * (cell_size + line) + line
    # Setting the font style and size of "Next Block"
    font_2 = pygame.font.SysFont('Arial', 20)
    font_width = int(font_2.size("Next Block")[0])
    font_height = int(font_2.size("Next Block")[1])
    # Setting the x and y coordinate of the text "Next Block"
    font_x = bg_cor1[0] + (bg_width - font_width)/2
    font_y = bg_cor1[1] + (bg_height - font_height)/2
    game_text(screen, font_2, font_x, font_y + 20, "Next Block", (104, 149, 191))
    '''
    Using the button_return function defined before to create a button on the lower right corner of the 
    screen. When player click the return button, the page will jump back to home page
    '''
    # button_return(screen, "return", 75 + 11 * (cell_size + line), 675, Home_page)


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

    def chk_rotation(self, block):
        '''
        This function is for checking whether the current block can rotate or not.

        **Parameters**

            block: *list*
                Each coordinate of four grids in this block.

        **Output**

           valid: *bool*
                Whether the rotation are valid (True) or not (False).
        '''
        for sq in block:
            # Check the feasibility by checking the position of grids one by one.
            if sq[0] < -4 or sq[0] > 5:
                # If any one of the grid in the block will get out of the board range, return False.
                # The x coordinate range of board is (-4,5).
                return False
        # After the loop, if there is no grid out of the range, return True
        return True

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
            # Check the feasibility by checking the position of grids one by one.
            if sq[1] + del_y > 22 or sq[0] + del_x < -4 or sq[0] + del_x > 5:
                '''
                If any one of the grid in the block will get out of the board range after the 
                delta x and delta y move step, return False.
                '''
                return False
        # After the loop, if there is no grid that will be out of the range, return True
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
            # Check the feasibility by checking the position of grids one by one.
            if (sq[0] + del_x, sq[1] + del_y) in self.done_area:
                '''
                If any one of the grid in the block will overlap with the grids landed 
                in the done list after the delta x and delta y move step, return False.
                This means the block cannot move this step.
                '''
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
                # If one of the squares in the block is out of the top range of the board, the game is over.
                return False
        return True

    def rotation(self):
        '''
        This function is for switching blocks to different forms in the shape list. Visually,
        the blocks are rotated in the game board.

        **Parameters**

            None

        **Output**

            block: *list*
                The block after rotation once
            block_id: *int*
                The corresponding index of the block after rotation
        '''
        # create a empty list to store squares in the block after rotation and movement
        ro_block = []
        # Get the initial index and store it for following index increasing
        index = self.block_id
        # Record the x and y direction movement of the block and apply the same movement to the block after rotation
        del_x = self.block[0][0] - self.block_shape[index][0][0]
        del_y = self.block[0][1] - self.block_shape[index][0][1]
        #
        if index + 1 <= len(self.block_shape) - 1:
            new_block = self.block_shape[index + 1]
            for sq in new_block:
                ro_block.append((sq[0] + del_x, sq[1] + del_y))
            if self.chk_rotation(ro_block):
                self.block = ro_block
                self.block_id = index + 1
        else:
            new_block = self.block_shape[0]
            for sq in new_block:
                ro_block.append((sq[0] + del_x, sq[1] + del_y))
            if self.chk_rotation(ro_block):
                self.block = ro_block
                self.block_id = 0
        return self.block, self.block_id


    def move(self, del_x, del_y):
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
    NB = None

    def create_next(self):
        if self.clear_num % 5 != 0 or self.clear_num == 0:
            # When clear row is not 5, 10, 15 and so on, the next block will be created in normal shape
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
        elif self.clear_num % 5 == 0 and self.clear_num != 0:
            '''
            When the clear row is 5, 10, 15 and so on, which also means the score reach every 500, the player get 
            a reward block which only has one little square.
            '''
            if self.score_jug % 5000 == 0:
                # To make sure the reward block shows only once for each 500 score.
                next_block = reward[0]
                next_shape = reward
                self.next_block = next_block
                self.next_shape = next_shape
                self.next_block_id = self.next_shape.index(self.next_block)
                new_color_ind = random.choice(len(colors))
                new_color = colors[new_color_ind]
                self.next_color = new_color
                self.score_jug += 1
                return self.next_block, self.next_shape, self.next_block_id, self.next_color
            else:
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
        bg_cor1 = (50 + 11 * (cell_size + line), 175)
        bg_width = 5 * (cell_size + line) + line
        bg_height = 7 * (cell_size + line) + line
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(bg_cor1[0], bg_cor1[1], bg_width, bg_height))
        for sq in self.next_block:
            line_corn1 = (50 + (sq[0] + 13) * (cell_size + line), 100 + (sq[1] + 9) * (cell_size + line))
            line_corn2 = (50 + (sq[0] + 14) * (cell_size + line), 100 + (sq[1] + 9) * (cell_size + line))
            line_corn3 = (50 + (sq[0] + 14) * (cell_size + line), 100 + (sq[1] + 10) * (cell_size + line))
            line_corn4 = (50 + (sq[0] + 13) * (cell_size + line), 100 + (sq[1] + 10) * (cell_size + line))
            corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
            pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
            pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
            pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
            pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
            pygame.draw.rect(screen, self.next_color, pygame.Rect(corn1[0], corn1[1], cell_size, cell_size))

    def create_new_block(self):
        self.block = self.next_block
        self.block_shape = self.next_shape
        # get the initial index of every new blocks for further block rotation function
        self.block_id = self.next_block_id
        self.color = self.next_color
        self.create_next()
        return self.block, self.color, self.block_shape

    def falling(self):
        if self.chk_move(0, 1):
            if self.chk_overlap(0, 1):
                self.move(0, 1)
                game = 1
                return game
            else:
                '''
                First, check whether the current block will overlap with the block below 
                If the block overlap with the block below, and this block is already out of the game board area,
                the game will stop.
                '''
                if self.chk_over():
                    for bol in self.block:
                        self.ex_color.append(self.color)
                        self.done_area.append(bol)
                    self.clear_row()
                    self.create_new_block()
                    game = 1
                    return game
                else:
                    for bol in self.block:
                        # Add the last block to done_area list
                        self.ex_color.append(self.color)
                        self.done_area.append(bol)
                    game = 2
                    return game
        else:
            for bol in self.block:
                self.ex_color.append(self.color)
                self.done_area.append(bol)
            self.clear_row()
            self.create_new_block()
            game = 1
            return game

    def key_control(self, del_x, del_y):
        if self.chk_move(del_x, del_y):
            if self.chk_overlap(del_x, del_y):
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
            self.whole_cor.append(row)  # generate all the coordinate of points into the whole coordinate list
            self.whole_cor.reverse()  # To make sure each row in this list is arranged from bottom to top
        for row in self.whole_cor:
            if self.chk_clear(row, self.done_area):
                # record the row number of the row that will be cleared.
                row_done = row[0][1]
                for i in row:
                    self.ex_color.pop(self.done_area.index(i))
                    self.done_area.remove(i)
                self.clear_num += 1
                self.score_jug = self.clear_num * 1000
                done_temp = []
                for bl in self.done_area[:]:
                    if bl[1] < row_done:
                        done_temp.append((bl[0], bl[1] + 1))
                        self.done_area.remove(bl)
                for i in done_temp:
                    self.done_area.append(i)

    def extra_row(self):
        new_done = []
        for sq in self.done_area:
            new_done.append((sq[0], sq[1] - 1))
        self.done_area = new_done
        for x in range(-4, 5):
            self.done_area.append((x, 22))
            self.ex_color.append((240, 166, 179))

    def draw_score(self, screen):
        bg_cor1 = (50 + 11 * (cell_size + line), 400)
        bg_width = 5 * (cell_size + line) + line
        bg_height = 2 * (cell_size + line) + line
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(bg_cor1[0], bg_cor1[1] + 55, bg_width, bg_height))
        font_2 = pygame.font.SysFont('Arial', 20)
        font_3 = pygame.font.SysFont('Cambria Math', 24)
        font_width = int(font_2.size("Score")[0])
        font_height = int(font_2.size("Score")[1])
        font_x = bg_cor1[0] + (bg_width - font_width) / 2
        font_y = bg_cor1[1] + 30
        font_width_s = int(font_3.size('Score: %d' % (self.clear_num * 100))[0])
        font_height_s = int(font_3.size('Score: %d' % (self.clear_num * 100))[1])
        font_x_s = bg_cor1[0] + (bg_width - font_width_s) / 2
        font_y_s = font_y + font_height_s + 25
        game_text(screen, font_2, font_x, font_y, "Score", (104, 149, 191))
        game_text(screen, font_3, font_x_s, font_y_s + 2, 'Score: %d' % (self.clear_num * 100), (178, 34, 34))

    def draw_block(self, cell_size, line, screen):
        if self.falling:
            for sq in self.block:
                line_corn1 = (50 + (sq[0] + 4) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                line_corn2 = (50 + (sq[0] + 5) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                line_corn3 = (50 + (sq[0] + 5) * (cell_size + line), 100 + (sq[1] + 3) * (cell_size + line))
                line_corn4 = (50 + (sq[0] + 4) * (cell_size + line), 100 + (sq[1] + 3) * (cell_size + line))
                corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
                pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
                pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
                pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
                pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
                pygame.draw.rect(screen, self.color, pygame.Rect(corn1[0], corn1[1], cell_size, cell_size))
            for pot in self.done_area:
                line_corn1 = (50 + (pot[0] + 4) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                line_corn2 = (50 + (pot[0] + 5) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                line_corn3 = (50 + (pot[0] + 5) * (cell_size + line), 100 + (pot[1] + 3) * (cell_size + line))
                line_corn4 = (50 + (pot[0] + 4) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
                pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
                pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
                pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
                pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
                pygame.draw.rect(screen, self.ex_color[self.done_area.index(pot)], pygame.Rect(corn1[0], corn1[1], cell_size, cell_size))


def level_1():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    Block = creat_block()
    block = Block[0]
    block_shape = Block[1]
    block_id = Block[2]
    screen_block1 = Blocks(block, block_shape, block_id)
    screen_block1.create_next()
    screen_block1.done_area = []
    screen_block1.ex_color = []
    font_level_small = pygame.font.SysFont('Arial', 25)
    font_level_large = pygame.font.SysFont('Arial', 30)
    w = int(font_level_small.size("return")[0])
    h = int(font_level_small.size("return")[1])
    x = 75 + 11 * (cell_size + line)
    y = 675
    move_time = 500
    time = pygame.time.get_ticks() + move_time
    game = 1
    pause = False
    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    if game == 1 and not pause:
                        screen_block1.key_control(-1, 0)
                elif event.key == K_RIGHT:
                    if game == 1 and not pause:
                        screen_block1.key_control(1, 0)
                elif event.key == K_DOWN:
                    if game == 1 and not pause:
                        screen_block1.key_control(0, 1)
                elif event.key == K_UP:
                    if game == 1 and not pause:
                        screen_block1.rotation()
                elif event.key == K_SPACE:
                    if game == 1:
                        pause = not pause
                elif event.key == K_RETURN:
                    if game == 2:
                        Block = creat_block()
                        block = Block[0]
                        block_shape = Block[1]
                        block_id = Block[2]
                        screen_block = Blocks(block, block_shape, block_id)
                        screen_block.done_area = []
                        screen_block.ex_color = []
                        screen_block.create_next()
                        game = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x < mouse[0] < x + w and y < mouse[1] < y + h:
                    Home_page()
        display_screen(screen)
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            game_text(screen, font_level_large, x, y, "return", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x, y, "return", (90, 167, 167))
        screen_block1.draw_score(screen)
        screen_block1.draw_block(cell_size, line, screen)
        screen_block1.draw_next(screen)
        mouse = pygame.mouse.get_pos()
        if game == 2:
            over_font = pygame.font.Font(None, 60)
            restart_font = pygame.font.Font(None, 40)
            black = (0, 0, 0)
            game_text(screen, over_font, 75, 250, "Game Over", black)
            game_text(screen, restart_font, 75, 375, "Press Enter to restart game", (226, 90, 83))
        pygame.display.update()
        if pause:
            time = pygame.time.get_ticks()
        if pygame.time.get_ticks() >= time:
            if game == 1 and not pause:
                time = pygame.time.get_ticks() + move_time
                game = screen_block1.falling()


def level_2():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    Block = creat_block()
    block = Block[0]
    block_shape = Block[1]
    block_id = Block[2]
    screen_block2 = Blocks(block, block_shape, block_id)
    screen_block2.create_next()
    screen_block2.done_area = []
    screen_block2.ex_color = []
    font_level_small = pygame.font.SysFont('Arial', 25)
    font_level_large = pygame.font.SysFont('Arial', 30)
    w = int(font_level_small.size("return")[0])
    h = int(font_level_small.size("return")[1])
    x = 75 + 11 * (cell_size + line)
    y = 675
    move_time = 600
    time = pygame.time.get_ticks() + move_time
    game = 1
    pause = False
    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    if game == 1 and not pause:
                        screen_block2.key_control(-1, 0)
                elif event.key == K_RIGHT:
                    if game == 1 and not pause:
                        screen_block2.key_control(1, 0)
                elif event.key == K_DOWN:
                    if game == 1 and not pause:
                        screen_block2.key_control(0, 1)
                elif event.key == K_UP:
                    if game == 1 and not pause:
                        screen_block2.rotation()
                elif event.key == K_SPACE:
                    if game == 1:
                        pause = not pause
                elif event.key == K_RETURN:
                    if game == 2:
                        Block = creat_block()
                        block = Block[0]
                        block_shape = Block[1]
                        block_id = Block[2]
                        screen_block = Blocks(block, block_shape, block_id)
                        screen_block.done_area = []
                        screen_block.ex_color = []
                        screen_block.create_next()
                        game = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x < mouse[0] < x + w and y < mouse[1] < y + h:
                    Home_page()
        display_screen(screen)
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            game_text(screen, font_level_large, x, y, "return", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x, y, "return", (90, 167, 167))
        screen_block2.draw_score(screen)
        screen_block2.draw_block(cell_size, line, screen)
        screen_block2.draw_next(screen)
        '''
        In level 2, For every 5 rows of blocks the player removes, 
        the block's fall speed increases by 50 milliseconds until the fastest speed.
        '''
        if screen_block2.clear_num % 5 == 0 and screen_block2.clear_num != 0 and screen_block2.clear_num <= 15:
            move_time -= 100
        if game == 2:
            over_font = pygame.font.Font(None, 60)
            restart_font = pygame.font.Font(None, 40)
            black = (0, 0, 0)
            game_text(screen, over_font, 75, 250, "Game Over", black)
            game_text(screen, restart_font, 75, 375, "Press Enter to restart game", (25, 25, 112))
        pygame.display.update()
        if pause:
            time = pygame.time.get_ticks()
        if pygame.time.get_ticks() >= time:
            if game == 1 and not pause:
                time = pygame.time.get_ticks() + move_time
                game = screen_block2.falling()


def level_3():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    Block = creat_block()
    block = Block[0]
    block_shape = Block[1]
    block_id = Block[2]
    screen_block3 = Blocks(block, block_shape, block_id)
    screen_block3.create_next()
    screen_block3.done_area = []
    screen_block3.ex_color = []
    font_level_small = pygame.font.SysFont('Arial', 25)
    font_level_large = pygame.font.SysFont('Arial', 30)
    w = int(font_level_small.size("return")[0])
    h = int(font_level_small.size("return")[1])
    x = 75 + 11 * (cell_size + line)
    y = 675
    move_time = 500
    time = pygame.time.get_ticks() + move_time
    game = 1
    pause = False
    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    if game == 1 and not pause:
                        screen_block3.key_control(-1, 0)
                elif event.key == K_RIGHT:
                    if game == 1 and not pause:
                        screen_block3.key_control(1, 0)
                elif event.key == K_DOWN:
                    if game == 1 and not pause:
                        screen_block3.key_control(0, 1)
                elif event.key == K_UP:
                    if game == 1 and not pause:
                        screen_block3.rotation()
                elif event.key == K_SPACE:
                    if game == 1:
                        pause = not pause
                elif event.key == K_RETURN:
                    if game == 2:
                        Block = creat_block()
                        block = Block[0]
                        block_shape = Block[1]
                        block_id = Block[2]
                        screen_block = Blocks(block, block_shape, block_id)
                        screen_block.done_area = []
                        screen_block.ex_color = []
                        screen_block.create_next()
                        game = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x < mouse[0] < x + w and y < mouse[1] < y + h:
                    Home_page()
        display_screen(screen)
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            game_text(screen, font_level_large, x, y, "return", (56, 82, 132))
        else:
            game_text(screen, font_level_small, x, y, "return", (90, 167, 167))
        screen_block3.draw_score(screen)
        screen_block3.draw_block(cell_size, line, screen)
        screen_block3.draw_next(screen)
        if (screen_block3.clear_num * 1000) % 2000 == 0 and screen_block3.clear_num != 0:
            screen_block3.extra_row()
            screen_block3.clear_num += 1
        if game == 2:
            over_font = pygame.font.Font(None, 60)
            restart_font = pygame.font.Font(None, 40)
            black = (0, 0, 0)
            game_text(screen, over_font, 75, 250, "Game Over", black)
            game_text(screen, restart_font, 75, 375, "Press Enter to restart game", (25, 25, 112))
        pygame.display.update()
        if pause:
            time = pygame.time.get_ticks()
        if pygame.time.get_ticks() >= time:
            if game == 1 and not pause:
                time = pygame.time.get_ticks() + move_time
                game = screen_block3.falling()


if __name__ == "__main__":
    Home_page()








