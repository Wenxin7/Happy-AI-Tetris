import random
import pygame
from numpy import *
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE

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
colors = [(255, 0, 0), (30, 144, 255), (255, 255, 0), (46, 139, 87), (160, 32, 240), (255, 165, 0), (255, 105, 180)]

# Define the game board
cell_size = 25
columns = 10
rows = 25
line = 1
board_width = columns * (cell_size + line) + line
board_height = rows * (cell_size + line) + line
screen_width = 500
screen_height = 800
board_start_x = (screen_width - board_width) // 2
board_start_y = screen_height - board_height



def game_text(screen, font, x, y, message, color):
    text = font.render(message, 1, color)
    screen.blit(text, (x, y))


def display_screen(screen):
    screen.fill((252, 230, 201))
    pygame.draw.rect(screen, (255, 250, 250),pygame.Rect(50, 100, board_width, board_height))
    for x in range(columns + 1):
        pygame.draw.line(screen, (0, 0, 0), (50 + x * (cell_size + line), 100), (50 + x * (cell_size + line), board_height + 99))
    for y in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (50, y * (cell_size + line) + 100), (board_width + 49, y * (cell_size + line) + 100))
    pygame.font.init()

    font_1 = pygame.font.SysFont('Arial', 12)
    font_width = int(font_1.size("Press SPACE to pause the game")[0])
    font_height = int(font_1.size("Press SPACE to pause the game")[1])
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(313, 595, font_width + 5, font_height + 5))
    game_text(screen, font_1, 318, 600, "Press SPACE to pause the game", (160, 32, 240))
    bg_cor1 = (50 + 11 * (cell_size + line), 100)
    bg_width = 5 * (cell_size + line) + line
    bg_height = 2 * (cell_size + line) + line
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(bg_cor1[0], bg_cor1[1], bg_width, bg_height))
    font_2 = pygame.font.SysFont('Arial', 20)
    font_width = int(font_2.size("Next Block")[0])
    font_height = int(font_2.size("Next Block")[1])
    font_x = bg_cor1[0] + (bg_width - font_width)/2
    font_y = bg_cor1[1] + (bg_height - font_height)/2
    game_text(screen, font_2, font_x, font_y, "Next Block", (160, 32, 240))


def creat_block():
    block_shape = random.choice(blocks)
    block = block_shape[0]
    block_id = block_shape.index(block)
    return block, block_shape, block_id


class Blocks(object):
    def __init__(self, block, block_shape,  block_id):
        self.color_ind = random.choice(len(colors))
        self.color = colors[self.color_ind]
        self.block_shape = block_shape
        self.block = block
        # The initial index of every new-born block
        self.block_id = block_id

    def __call__(self):
        return self.block

    def rotation(self):
        ro_block = []
        index = self.block_id
        # Record the movement of the block and apply the same movement to the block after rotation
        del_x = self.block[0][0] - self.block_shape[index][0][0]
        del_y = self.block[0][1] - self.block_shape[index][0][1]
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

    def chk_rotation(self, block):
        for sq in block:
            if sq[0] < -4 or sq[0] > 5:
                return False
        return True

    def chk_move(self, del_x, del_y):
        for sq in self.block:
            if sq[1] + del_y > 22 or sq[0] + del_x < -4 or sq[0] + del_x > 5:
                return False
        return True

    def chk_overlap(self, del_x, del_y):
        for sq in self.block:
            if (sq[0] + del_x, sq[1] + del_y) in self.done_area:
                return False
        return True

    def chk_over(self):
        # check whether there are done blocks already in the top row
        for sq in self.block:
            if sq[1] <= -2:
                return False
        return True

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
        bg_height = 5 * (cell_size + line) + line
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(bg_cor1[0], bg_cor1[1], bg_width, bg_height))
        font_2 = pygame.font.SysFont('Arial', 20)
        font_3 = pygame.font.SysFont('Cambria Math', 24)
        font_width = int(font_2.size("Score")[0])
        font_height = int(font_2.size("Score")[1])
        font_x = bg_cor1[0] + (bg_width - font_width) / 2
        font_y = bg_cor1[1] + 30
        font_width_s = int(font_3.size('Score:%05d' % (self.clear_num * 100))[0])
        font_height_s = int(font_3.size('Score:%05d' % (self.clear_num * 100))[1])
        font_x_s = bg_cor1[0] + (bg_width - font_width_s) / 2
        font_y_s = font_y + font_height_s + 25
        game_text(screen, font_2, font_x, font_y, "Score", (160, 32, 240))
        game_text(screen, font_3, font_x_s, font_y_s, 'Score:%05d' % (self.clear_num * 100), (178, 34, 34))


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
    move_time = 300
    time = pygame.time.get_ticks() + move_time
    game = 1
    pause = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    if game == 1 and not pause:
                        screen_block.key_control(-1, 0)
                elif event.key == K_RIGHT:
                    if game == 1 and not pause:
                        screen_block.key_control(1, 0)
                elif event.key == K_DOWN:
                    if game == 1 and not pause:
                        screen_block.key_control(0, 1)
                elif event.key == K_UP:
                    if game == 1 and not pause:
                        screen_block.rotation()
                elif event.key == K_SPACE:
                    if game == 1:
                        pause = not pause
        display_screen(screen)
        screen_block.draw_score(screen)
        screen_block.draw_block(cell_size, line, screen)
        screen_block.draw_next(screen)
        if game == 2:
            over_font = pygame.font.Font(None, 60)
            black = (0, 0, 0)
            game_text(screen, over_font, 75, 250, "Game Over", black)
        pygame.display.update()
        if pause:
            time = pygame.time.get_ticks()
        if pygame.time.get_ticks() >= time:
            if game == 1 and not pause:
                time = pygame.time.get_ticks() + move_time
                game = screen_block.falling()






main()










