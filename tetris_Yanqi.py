import copy
block_dir = {
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
# block type: Z,T,S,O... block_id:第几个列表 
# 已经定义好 screen_matrix, screen_wide, screen_hight: 以块数为单位
# screen_matrix: 已经摆好的所有块的坐标
# center 是坐标-代表屏幕上可以放置的定位中心

columns = 10    # screen wide
rows = 25    # screen height
done_area = [(-4,20),(-4,21),(-4,22),(-3,22),
            (-3,18),(-3,19),(-3,20),(-3,21),
            (-2,21),(-2,22),(-1,21),(-1,22),
            (-1,20),(0,20),(0,21),(1,21),
            (0,22),(1,22),(2,22),(3,22),
            (1,20),(2,20),(2,21),(3,21),
            (4,21),(4,22),(5,21),(5,22),
            (3,20),(4,20),(5,19),(5,20)]   # 放入块的坐标


def judging_centers(done_area):
    # 重新建立坐标系
    def block_to_matrix():
        screen_matrix = [[None] * columns for i in range(rows)]
        for done in done_area:
            screen_matrix[done[1]+2][done[0]+4] = 0
        return screen_matrix

    screen_matrix = block_to_matrix()
    
    def wrong_position(block_type, block_id, fall_position):
        # 要落下的方块的四格位置
        all_block_position = [(cube[0] + fall_position[0], cube[1] + fall_position[1]) for cube in block_dir[block_type][block_id]]
        for cube_co in all_block_position:
            if (cube_co[0] < 0 or cube_co[1] < 0 or cube_co[0]>columns-1 or cube_co[1]>rows-1):
                return True
            if screen_matrix[cube_co[1]][cube_co[0]] != None:
                return True
        return False

    # get all possible position to all for blocks
    centerList = []
    for b_type in block_dir.keys():
        for block_id in range(len(block_dir[b_type])): 
            for w in range(columns):
                for h in range(rows):
                    if wrong_position(b_type, block_id, (w, h)) == False and wrong_position(b_type, block_id, (w, h+1)) == True:
                        centerList.append([b_type, block_id, (w, h)])
    

    # count scores     
    for centerlist in centerList:
        # get LandingHeight
        LandingHeight = rows - centerlist[2][1]
        centerlist.append(LandingHeight)    # LandingHeight 作为表中第四列
    
        # get eliminate contribution
        matrix_after = copy.deepcopy(screen_matrix)    # 得到下落之后matrix
        new_block_position = []    # 方块落下之后四个cube坐标list
        for cube_pos in block_dir[centerlist[0]][centerlist[1]]:
            new_block_position.append((cube_pos[0]+centerlist[2][0], cube_pos[1]+centerlist[2][1]))

        for new_cor in new_block_position:
            matrix_after[new_cor[1]][new_cor[0]] = 0   

        eliminate_line = 0
        useful_cube = 0
        elimination_contribution = 0
        for i in range(rows-1, 0, -1):
            t = 0
            for j in range(columns):
                if matrix_after[i][j] != None:
                    t += 1
            if t == columns:
                eliminate_line += 1
                for b_posi in new_block_position:
                    if b_posi[1] == i:
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
        whole_point = -45*centerlist[3] + 34*centerlist[4] - 32*centerlist[5] - 98*centerlist[6] -79*centerlist[7] -34*centerlist[3]
        centerlist.append(whole_point)    # whole_point 作为表中第十列

    # choose the optimal block with rotation and center:
    largest_point_block = centerList[0]
    for centerlist in centerList:
        if centerlist[9] > largest_point_block[9]:
            largest_point_block = centerlist
    # 返回块种类，块的旋转方式ID，块matrix坐标，块落在坐标系中的坐标
    return largest_point_block[0], largest_point_block[1], largest_point_block[2], (largest_point_block[2][0]-4, largest_point_block[2][1]-2)

print(judging_centers(done_area))
