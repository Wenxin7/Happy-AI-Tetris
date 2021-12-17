import unittest
import tetris_ai_optimize
import player


class TestStringMethods(unittest.TestCase):
    def check_chk_move(self):
        '''
        This function will check whether the chk_move function judge the block have fall the the bottom
        correctly 
        '''
        block = [(-1, 21), (0, 21), (0, 22), (1, 22)]
        block_shape = 'Z'
        block_id = 1
        self.assertEqual(
            (player.Block(block, block_shape, block_id).chk_move(0, 1)), (False))

    def check_chk_rotation(self):
        '''
        This function will check whether the chk_rotation function will judge block can or cannot 
        rotate correctly
        '''
        block = [(4, 22), (5, 22), (5, 21), (5, 20)]
        block_shape = 'L'
        block_id = 3
        self.assertEqual(
            (player.Block(block, block_shape, block_id).chk_rotation(block)), (False))

    def check_chk_overlap(self):
        '''
        This function will check whether the function could judge current block will overlap with 
        landed blocks or not correctly
        '''
        done_area = [(-4, 21), (-3, 21), (-2, 21), (-1, 21)]
        block = [(-1, 21), (0, 21), (0, 22), (1, 22)]
        block_shape = 'I'
        block_id = 1
        self.assertEqual(
            (player.Block(block, block_shape, block_id).chk_overlap(0, 1)), (False))

    def check_judging_centers(self):
        '''
        This function will check whether the ai part will gave suitable block and ratation type
        '''
        done_area = [(-1, 21), (0, 21), (0, 22), (1, 22)]
        block_shape = [[(0, -4), (0, -3), (0, -2), (0, -1)],
                       [(-1, -3), (0, -3), (1, -3), (2, -3)]]
        correct_block = ('I', 1, (3, 25), [
                         (-1, -3), (0, -3), (1, -3), (2, -3)])
        self.assertEqual((tetris_ai_optimize.judging_centers(
            done_area, block_shape)), correct_block)


if __name__ == '__main__':

    unittest.main()
