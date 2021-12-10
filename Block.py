# Block
import random
from random import randrange
import pygame
import numpy as np
from numpy import *

# Define block shapes
T = [[(-1, 0), (0, 0), (1, 0), (0, -1)],
           [(0, -1), (0, 0), (1, 0), (0, 1)],
           [(-1, 0), (0, 0), (1, 0), (0, 1)],
           [(0, -1), (0, 0), (-1, 0), (0, 1)]]
Z = [[(-1, -1), (0, -1), (0, 0), (1, 0)],
           [(0, -1), (0, 0), (-1, 0), (-1, 1)]]
S = [[(1, 1), (0, -1), (0, 0), (-1, 0)],
           [(-1, -1), (-1, 0), (0, 0), (0, 1)]]
I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
          [(-1, 0), (0, 0), (1, 0), (2, 0)]]
L = [[(0, -2), (0, -1), (0, 0), (1, 0)],
           [(2, 0), (1, 0), (0, 0), (0, 1)],
           [(0, 2), (0, 1), (0, 0), (-1, 0)],
           [(-2, 0), (-1, 0), (0, 0), (0, -1)]]
J = [[(0, -2), (0, -1), (0, 0), (-1, 0)],
           [(2, 0), (1, 0), (0, 0), (0, -1)],
           [(0, 2), (0, 1), (0, 0), (1, 0)],
           [(-2, 0), (-1, 0), (0, 0), (0, 1)]]
O = [[(-1, -1), (-1, 0), (0, -1), (0, 0)]]

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
screen_height = 750
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
    pygame.draw.rect(screen, (255, 250, 250),pygame.Rect(50, 50, board_width, board_height))
    for x in range(columns + 1):
        pygame.draw.line(screen, (0, 0, 0), (50 + x * (cell_size + line), 50), (50 + x * (cell_size + line), board_height + 49))
    for y in range(rows + 1):
        pygame.draw.line(screen, (0, 0, 0), (50, y * (cell_size + line) + 50), (board_width + 49, y * (cell_size + line) + 50))
    pygame.font.init()
    font1 = pygame.font.SysFont('arial', 60)
    font2 = pygame.font.SysFont('arial', 72) # bigger font for "GAME OVER"


def main():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Happy AI Tetris')
    display_screen(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


class Blocks(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_block(self):
        block_shape = random.choice(blocks)
        block = block_shape[0]
        return block

    def rotation(self, block):
        block = np.rot90(block, -1)
        return block

    def move(self, x_move, y_move):
        self.x = self.x + x_move
        self.y = self.y + y_move


class game_block():
    done_area = [] #fallen blocks
    cur_block = None # falling block

    def __init__(self, screen, block_size, position, color):
        self.screen = screen
        self.x, self.y, self.width, self.height = position
        self.block_size = block_size
        self.screen_color = color

    def creat_cur_block(self):
        block = Blocks(board_width-len(shape[0]//2), 0, random.randint(0, 6))
        cur_block = block.get_block()
        self.cur_block = cur_block

    def falling(self):
        self.cur_block.move(0, 1)

    # def draw_block(self):



A = Blocks(1, 2, colors[1])
B = A.get_block()









