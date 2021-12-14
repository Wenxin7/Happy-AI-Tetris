import copy
import random
import pygame
from numpy import *
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN

columns = 10    # screen wide
rows = 25    # screen height


def judging_centers(done_area):
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
    # 重新建立坐标系
    def block_to_matrix():
        screen_matrix = [[None] * columns for i in range(rows)]
        for done in done_area:
            screen_matrix[done[1]+2][done[0]+4] = 0
        return screen_matrix

    screen_matrix = block_to_matrix()
    # print(screen_matrix)
    def wrong_position(block_type, block_id, fall_position):
        # 要落下的方块的四格位置
        all_block_position = [(cube[0] + fall_position[0], cube[1] + fall_position[1]) for cube in block_dir[block_type][block_id]]
        for cube_co in all_block_position:
            if cube_co[0] < -4:
                return True
            if cube_co[1] < -2:
                return True
            if cube_co[0]> 5:
                return True
            if cube_co[1]>22:
                return True
            if screen_matrix[cube_co[1]+2][cube_co[0]+4] != None:
                return True
        return False

    # get all possible position to all for blocks
    centerList = []
    for b_type in block_dir.keys():
        for block_id in range(len(block_dir[b_type])): 
            for w in range(-4, 5):
                for h in range(25, 0, -1):
                    if (wrong_position(b_type, block_id, (w, h)) == False) and (wrong_position(b_type, block_id, (w, h+1)) == True):
                        centerList.append([b_type, block_id, (w, h)])

    

    # count scores     
    for centerlist in centerList:

        # get LandingHeight
        h_list = []
        for cor in block_dir[centerlist[0]][centerlist[1]]:
            h_list.append(cor[1] + centerlist[2][1])
        LandingHeight = 23 - min(h_list)
        centerlist.append(LandingHeight)    # LandingHeight 作为表中第四列

        
        # 得到下落之后matrix
        matrix_after = [[None] * columns for i in range(rows)]
        for done in done_area:
            matrix_after[done[1]+2][done[0]+4] = 0
        for new_cor in block_dir[centerlist[0]][centerlist[1]]:
            n_x = new_cor[0] + centerlist[2][0]
            n_y = new_cor[1] + centerlist[2][1]
            matrix_after[n_y+2][n_x+4] = 0
        
        # print(matrix_after)

        # get eliminate contribution

        new_block_position = []    # 方块落下之后四个cube坐标list
        for cube_pos in block_dir[centerlist[0]][centerlist[1]]:
            new_block_position.append((cube_pos[0]+centerlist[2][0], cube_pos[1]+centerlist[2][1])) 

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
        centerlist.append(elimination_contribution)    # elimination_contribution 作为表中第五列

        # get BroadRollTrandition
        roll_transition_times = 0
        for i in range(rows-1, 0, -1):
            for j in range(columns-1):
                if (matrix_after[i][j] == None and matrix_after[i][j + 1] != None) or (matrix_after[i][j] != None and matrix_after[i][j + 1] == None):
                    roll_transition_times += 1
        centerlist.append(roll_transition_times)    # roll_transition_times 作为表中第六列

        # get BroadColTrandition
        col_transition_times = 0
        for j in range(columns):
            for i in range(rows-1, 1, -1):
                if (matrix_after[i][j] == None and matrix_after[i-1][j] != None) or (matrix_after[i][j] != None and matrix_after[i-1][j] == None):
                    col_transition_times += 1
        centerlist.append(col_transition_times)    # col_transition_times 作为表中第七列
    
        # get empty_holes
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
        centerlist.append(empty_holes)    # empty_holes 作为表中第八列

        # get wells_number
        wells_number = 0
        wall_brick = 0
        for i in range (columns):
            for j in range(rows):
                if matrix_after[j][i] == None:
                    if (i == 0) and (matrix_after[j][i+1] != None):
                        wall_brick += 1
                    elif (i>0) and (i< columns-1) and (matrix_after[j][i-1] != None) and (matrix_after[j][i+1] != None):
                        wall_brick += 1
                    elif (i == columns-1) and (matrix_after[j][i-1] != None):
                       wall_brick += 1
                else:
                    wells_number += ((wall_brick +1)*wall_brick/2)
                    wall_brick = 0
        centerlist.append(wells_number)    # wells_number 作为表中第九列

        # get whole point of each center position of a kind rotation
        whole_point = -45*centerlist[3] + 100*centerlist[4] - 32*centerlist[5] - 98*centerlist[6] -79*centerlist[7] -34*centerlist[3]
        centerlist.append(whole_point)    # whole_point 作为表中第十列
        print(centerlist)

    # choose the optimal block with rotation and center:
    # largest_point_block = centerList[0]
    # for centerlist in centerList:
    #     if centerlist[9] > largest_point_block[9]:
    #         largest_point_block = centerlist
    point_list = []
    for centerlist in centerList:
        point_list.append(centerlist[9])
        
        max_index = point_list.index(max(point_list))
    
    largest_point_block = centerList[max_index]
    print(largest_point_block)

    # 返回块种类，块的旋转方式ID，块落在坐标系中的坐标(dlt_x, dlt_y), 块的原始点
    return largest_point_block[0], largest_point_block[1], largest_point_block[2], block_dir[largest_point_block[0]][largest_point_block[1]]
# print(judging_nextstep(done_area))
# raise Exception
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
fps = 60


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
    block_id = block_shape.index(block)
    # block_shape = [[(-1, -3), (0, -3), (1, -3), (0, -4)],
    #                     [(0, -4), (0, -3), (1, -3), (0, -2)],
    #                     [(-1, -3), (0, -3), (1, -3), (0, -2)],
    #                     [(0, -4), (0, -3), (-1, -3), (0, -2)]]
    # block = block_shape[0]
    # block_id = block_shape.index(block)

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

    def creat_new_block(self):
        # Z = [[(-1, -4), (0, -4), (0, -3), (1, -3)],[(0, -4), (0, -3), (-1, -3), (-1, -2)]]
        # if len(self.done_area) < 4:
        #     new_block = [[(-1, -3), (0, -3), (1, -3), (0, -4)],
        #                 [(0, -4), (0, -3), (1, -3), (0, -2)],
        #                 [(-1, -3), (0, -3), (1, -3), (0, -2)],
        #                 [(0, -4), (0, -3), (-1, -3), (0, -2)]]
            # for list in new_block:
            #     for cor in list:
            #         cor[0] = cor[0] - 3
            # self.block = new_block
            # new_shape = [(-1, -3), (0, -3), (1, -3), (0, -2)]
            # self.block_shape = new_shape
            # new_Block = creat_block()
            # new_block = new_Block[0]
            # self.block = new_block
            # new_shape = new_Block[1]
            # self.block_shape = new_shape
        d_x = judging_centers(self.done_area)[2][0]
        block_cor = judging_centers(self.done_area)[3]
        new_cor = []
        for co in block_cor:
            
            n_x = co[0] + d_x
            n_y = co[1]
            new_cor.append((n_x, n_y))         
        self.block = new_cor
        # for b_type in blocks:
        #     for rotation_type in blocks(b_type):
        #         if new_cor == rotation_type:
        #             self.block = blocks(b_type)

        self.block_shape = new_cor
        # new_Block = creat_block()
        # new_block = new_Block[0]
        # self.block = new_block
        # new_shape = new_Block[1]
        # self.block_shape = new_shape
        # # get the initial index of every new blocks for further block rotation function
        # self.block_id = self.block_shape.index(self.block)
        new_color_ind = random.choice(len(colors))
        new_color = colors[new_color_ind]
        self.color = new_color
        return self.block, self.color, self.block_shape

    def falling(self):
       
        if self.chk_move(0, 1):
            if self.chk_overlap(0, 1):
                self.move(0, 1)

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
                    self.creat_new_block()
        else:
            for bol in self.block:
                self.ex_color.append(self.color)
                self.done_area.append(bol)
            self.clear_row()
            self.creat_new_block()

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
    move_time = 100
    time = pygame.time.get_ticks() + move_time
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # elif event.type == pygame.KEYDOWN:
                # if event.key == K_LEFT:
                #     screen_block.key_control(-1, 0)
                # elif event.key == K_RIGHT:
                #     screen_block.key_control(1, 0)
                # elif event.key == K_DOWN:
                #     screen_block.key_control(0, 1)
                # elif event.key == K_UP:
                #     screen_block.rotation()
        display_screen(screen)
        screen_block.draw_block(cell_size, line, screen)
        pygame.display.update()
        if pygame.time.get_ticks() >= time:
            time += move_time
            screen_block.falling()





main()