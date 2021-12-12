
from math import copysign


block = {
        'I': [[(0, -1), (0, 0), (0, 1), (0, 2)],
            [(-1, 0), (0, 0), (1, 0), (2, 0)]], 
        'J': [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
            [(-1, 0), (0, 0), (0, 1), (0, 2)],
            [(0, 1), (0, 0), (1, 0), (2, 0)],
            [(0, -2), (0, -1), (0, 0), (1, 0)]], 
        'L': [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
            [(1, 0), (0, 0), (0, 1), (0, 2)],
            [(0, -1), (0, 0), (1, 0), (2, 0)],
            [(0, -2), (0, -1), (0, 0), (-1, 0)]], 
        'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]], 
        'S': [[(-1, 0), (0, 0), (0, 1), (1, 1)],
            [(1, -1), (1, 0), (0, 0), (0, 1)]], 
        'T': [[(0, -1), (0, 0), (0, 1), (-1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(0, -1), (0, 0), (0, 1), (1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, -1)]], 
        'Z': [[(0, -1), (0, 0), (1, 0), (1, 1)],
            [(-1, 0), (0, 0), (0, -1), (1, -1)]]
    }
# block type: Z,T,S,O... rotation_type:第几个列表 
# 已经定义好 screen_matrix, screen_wide, screen_hight: 以块数为单位
# screen_matrix: 已经摆好的所有块的坐标
# center 是坐标-代表屏幕上可以放置的定位中心
def wrong_position(block_type, rotation_type, center):
    all_block_position = [(cube[0] + center[0], cube[1] + center[1]) for cube in block[block_type][rotation_type]]
    for cube_co in all_block_position:
        if (cube_co[0] < 0 or cube_co[1] < 0 or cube_co[0]>screen_wide or cube_co[1]>screen_hight):
            return True
        if screen_matrix[cube_co[1]][cube_co[0]] != None:
            return True
    return False

def judging_centers():

    # get all_possible_centers
    centerList = []
    for b_type in range(len(block)):
        for rot_type in range(len(block[b_type])): 
            for w in range(screen_wide):
                for h in range(screen_height):
                    if wrong_position(b_type, rot_type, (w, h)) == False and wrong_position(b_type, rot_type, (w, h+1)) == True:
                        centerList.append([b_type, rot_type, (w, h)])
    

    # count scores
        
    for centerlist in centerList:
        # get LandingHeight
        LandingHeight = screen_hight - centerlist[2][1]
        centerlist.append(LandingHeight)    # LandingHeight 作为表中第四列
    
        # get eliminate parameter
        matrix_after = copy.deepcopy(screen_matrix)
        new_block_position = []    # 方块落下之后四个cube坐标list
        for cube_pos in block[centerlist[0][1]]:
            new_block_position.append((cube_pos[0]+centerlist[2][0], cube_pos[1]+centerlist[2][1]))

        matrix_after.append()    # ！！！应该是将颜色加入到坐标系中

        elimi_line = 0
        useful_cube = 0
        elimination_contribution = 0
        for i in range(screen_height-1, 0, -1):
            t = 0
            for j in range(screen_wide):
                if matrix_after[i][j] != None:
                    t += 1
            if t == screen_wide:
                elimi_line += 1
                for b_posi in new_block_position:
                    if b_posi[1] == i:
                        useful_cube += 1
        elimination_contribution = elimi_line * useful_cube
        centerlist.append(elimination_contribution)    # elimination_contribution 作为表中第五列

        # get BroadRollTrandition
        roll_transition_times = 0
        for i in range(screen_height-1, 0, -1):
            for j in range(screen_wide-1):
                if (matrix_after[i][j] == None and matrix_after[i][j + 1] != None) or (matrix_after[i][j] != None and matrix_after[i][j + 1] == None):
                    roll_transition_times += 1
        centerlist.append(roll_transition_times)    # roll_transition_times 作为表中第六列

        # get BroadColTrandition
        col_transition_times = 0
        for j in range(screen_wide):
            for i in range(screen_height-1, -1, -1):
                if (matrix_after[i][j] == None and matrix_after[i+1][j] != None) or (matrix_after[i][j] != None and matrix_after[i+1][j] == None):
                    col_transition_times += 1
        centerlist.append(col_transition_times)    # col_transition_times 作为表中第七列
    
        # get empty_holes
        empty_holes = 0
        for j in range(screen_wide):
            t = None
            for i in range(screen_height):
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
        for i in range (screen_wide):
            for j in range(screen_hight):
                if matrix_after[j][i] == None:
                    if (i == 0 or matrix_after[j][i-1] != None) and (i == screen_wide-1 or matrix_after[j][i+1] != None):
                       wall_brick += 1
                    else:
                        wells_number += ((wall_brick +1)*wall_brick/2)
                        wall_brick = 0
        centerlist.append(wells_number)    # wells_number 作为表中第九列

        # get whole point of each center position of a kind rotation
        whole_point = -45*centerlist[3] + 34*centerlist[4] - 32*centerlist[5] - 98*centerlist[6] -79*centerlist[7] -34*centerlist[3]
        centerlist.append(whole_point)    # whole_point 作为表中第十列

    # choose the optimal block with rotation and center:
    largest_point_block = centerList[0]
    for centerlist in centerList:
        if centerlist[9] > largest_point_block[9]:
            largest_point_block = centerlist
    
    return largest_point_block


