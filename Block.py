# Block
import random
from random import randrange
import pygame
import numpy as np
from numpy import *

# Define block shapes
T = array([[0, 1, 0],
           [1, 1, 1]],)
Z = array([[1, 1, 0],
           [0, 1, 1]])
S = array([[0, 1, 1],
           [1, 1, 0]])
I = array([[1, 1, 1, 1]])
L = array([[1, 0],
           [1, 0],
           [1, 1]])
J = array([[0, 1],
           [0, 1],
           [1, 1]])
O = array([[1, 1],
           [1, 1]])

blocks = [T, Z, S, I, L, J, O]

# Define the color
colors = [(255, 0, 0), (30, 144, 255), (255, 255, 0), (46, 139, 87), (160, 32, 240), (255, 165, 0), (255, 105, 180)]

# Define the game board
cell_size = 20
columns = 10
rows = 25
line = 1
board_width = columns * (cell_size + line) + line
board_height = rows * (cell_size + line) + line
screen_width = 500
screen_height = 700
board_start_x = (screen_width - board_width) // 2
board_start_y = screen_height - board_height
fps = 60



def get_board():
    board = [[0 for x in range(10)] for x in range(25)]
    return board


def display_screen(screen):
    screen.fill((252, 230, 201))
    for x in range(columns):
        pygame.draw.line(screen, (0, 0, 0), (x * cell_size, 0), (x * cell_size, board_height))
    for y in range(rows):
        pygame.draw.line(screen, (0, 0, 0), (0, y * cell_size))
    pygame.font.init()
    font1 = pygame.font.SysFont('arial', 60)
    font2 = pygame.font.SysFont('arial', 72) # bigger font for "GAME OVER"


def game_text(screen, font, x, y, text, color):
    text = font.render('AI Tetris', 1, (139, 28, 98))
    screen.blit(text, (x, y))



def main():
    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((screen_height, screen_width))
    pygame.display.set_caption('Happy Tetris')


class Blocks(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def get_block(self):
        block = random.choice(blocks)
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

    def draw_block(self):











A = Blocks(1, 2, T, colors)
B = A.shape
C = A.rotation(T)
print(C)

