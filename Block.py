# Block
import random
import pygame
from numpy import *
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

# Define block shapes
T = [[(-1, -3), (0, -3), (1, -3), (0, -4)],
     [(0, -4), (0, -3), (1, -3), (0, -2)],
     [(-1, -3), (0, -3), (1, -3), (0, -2)],
     [(0, -4), (0, -3), (-1, -3), (0, -2)]]
Z = [[(-1, -4), (0, -4), (0, -3), (1, -3)],
     [(0, -4), (0, -3), (-1, -3), (-1, -2)]]
S = [[(1, -4), (0, -4), (0, -3), (-1, -3)],
     [(1, -2), (1, -3), (0, -2), (0, -4)]]
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
fps = 60



def get_board():
    board = [[0 for x in range(10)] for x in range(25)]
    return board


def game_text(screen, font, x, y, text, color):
    text = font.render('AI Tetris', 1, (139, 28, 98))
    screen.blit(text, (x, y))


def display_screen(screen):
    screen.fill((252, 230, 201))
    pygame.draw.rect(screen, (255, 250, 250),pygame.Rect(50, 100, board_width, board_height))
    for x in range(columns + 1):
        pygame.draw.line(screen, (0, 0, 0), (50 + x * (cell_size + line), 100), (50 + x * (cell_size + line), board_height + 99))
    for y in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (50, y * (cell_size + line) + 100), (board_width + 49, y * (cell_size + line) + 100))
    pygame.font.init()
    font1 = pygame.font.SysFont('arial', 60)
    font2 = pygame.font.SysFont('arial', 72)  # bigger font for "GAME OVER"


def creat_block():
    block_shape = random.choice(blocks)
    block = block_shape[0]
    return block, block_shape


class Blocks(object):
    def __init__(self, block, block_shape):
        self.color_ind = random.choice(len(colors))
        self.color = colors[self.color_ind]
        self.block_shape = block_shape
        self.block = block

    def __call__(self):
        return self.block

    def rotation(self):
        index = self.block.index
        block = self.block_shape[index + 1]
        return block

    def chk_fall(self, del_x, del_y):
        for sq in self.block:
            if sq[1] + del_y > 22:
                return False
        return True

    def chk_overlap(self, del_x, del_y):
        for sq in self.block:
            for done in self.done_area:
                if (sq[0] + del_x, sq[1] + del_y) in done:
                    return False
        return True

    def chk_over(self):
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

    done_area = [] #fallen blocks
    cur_block = None # falling block
    ex_color = []

    def creat_new_block(self):
        new_block = creat_block()[0]
        self.block = new_block
        new_color_ind = random.choice(len(colors))
        new_color = colors[new_color_ind]
        self.color = new_color
        return self.block, self.color

    def falling(self):
        if self.chk_fall(0, 1):
            if self.chk_overlap(0, 1):
                self.move(0, 1)
            else:
                '''
                Check whether the current block 
                '''
                if self.chk_over():
                    self.ex_color.append(self.color)
                    self.done_area.append(self.block)
                    self.creat_new_block()
        else:
            self.ex_color.append(self.color)
            self.done_area.append(self.block)
            self.creat_new_block()

    # def key_control(self, del_x, del_y):


    def draw_block(self, cell_size, line, screen):
        if self.falling:
            for sq in self.block:
                line_corn1 = (50 + (sq[0] + 4) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                line_corn2 = (50 + (sq[0] + 5) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                line_corn3 = (50 + (sq[0] + 5) * (cell_size + line), 100 + (sq[1] + 3) * (cell_size + line))
                line_corn4 = (50 + (sq[0] + 4) * (cell_size + line), 100 + (sq[1] + 2) * (cell_size + line))
                corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
                pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
                pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
                pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
                pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
                pygame.draw.rect(screen, self.color, pygame.Rect(corn1[0], corn1[1], cell_size, cell_size))
        for sq in self.done_area:
            for pot in sq:
                line_corn1 = (50 + (pot[0] + 4) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                line_corn2 = (50 + (pot[0] + 5) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                line_corn3 = (50 + (pot[0] + 5) * (cell_size + line), 100 + (pot[1] + 3) * (cell_size + line))
                line_corn4 = (50 + (pot[0] + 4) * (cell_size + line), 100 + (pot[1] + 2) * (cell_size + line))
                corn1 = (line_corn1[0] + 1, line_corn1[1] + 1)
                pygame.draw.line(screen, (0, 0, 0), line_corn1, line_corn2)
                pygame.draw.line(screen, (0, 0, 0), line_corn2, line_corn3)
                pygame.draw.line(screen, (0, 0, 0), line_corn3, line_corn4)
                pygame.draw.line(screen, (0, 0, 0), line_corn4, line_corn1)
                pygame.draw.rect(screen, self.ex_color[self.done_area.index(sq)], pygame.Rect(corn1[0], corn1[1], cell_size, cell_size))


def main():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    block = creat_block()[0]
    block_shape = creat_block()[1]
    screen_block = Blocks(block, block_shape)
    move_time = 100
    time = pygame.time.get_ticks() + move_time
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        display_screen(screen)
        screen_block.draw_block(cell_size, line, screen)
        pygame.display.update()
        if pygame.time.get_ticks() >= time:
            time += move_time
            screen_block.falling()





main()










