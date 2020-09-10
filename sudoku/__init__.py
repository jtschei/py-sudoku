import logging
import random
import itertools
from copy import deepcopy

logger = logging.getLogger()

class Puzzle:
    def __init__(self, board=None):
        logger.debug("creating puzzle")
        if board is None:
            self.reset_board()
        else:
            self.board = deepcopy(board)

    def reset_board(self):
        logger.debug("resetting board")
        self.board = [[0] * 9 for i in range(9)]

    def initialize_board(self):
        logger.debug("initializing board")
        v: int = 0
        for x in range(0,9):
            for y in range(0,9):
                if x % 3 == 0 and y == 0:
                    v = int(x/3)
                self.set_position(x,y,v % 9 + 1)
                v = v+1
            v = v + 3

    def shuffle_board(self):
        logger.debug("shuffling board")

        #decide shift up/down/left/right
        #get shared points 
        shift_direction = random.randint(0,4) 
        to_shift = Puzzle.get_swaps()
        if shift_direction == 0:
            self.shift_left(to_shift)
        elif shift_direction == 1:
            self.shift_right(to_shift)
        elif shift_direction == 2:
            self.shift_up(to_shift)
        elif shift_direction == 3:
            self.shift_down(to_shift)
            pass
        else:
            raise ValueError()
         
    def dummy(self):
        swap1 = Puzzle.get_swaps()
        swap2 = Puzzle.get_swaps()
        while(len(list(set(swap1) & set(swap2))) > 0):
            logger.debug("reswapping")
            swap2 = Puzzle.get_swaps()
        swaps = list()
        for s in swap1:
            swaps.append(s)
        for s in swap2:
            swaps.append(s)
        logger.debug(f"swaps={swaps}")
        for position_changes in itertools.permutations(swaps,9):
            logger.debug(f"position_changes -> {position_changes}")
            if self.swap_positions(position_changes):
                return
        #for c in position_changes:
        #    self.swap_position(c[0][0],c[0][1],c[1][0],c[1][1])


    @staticmethod
    def get_swaps():
        logger.debug("getting swaps")
        spots=list()
        #box0,0
        x00 = random.randint(0,2)
        y00 = random.randint(0,2)
        spots.append((x00,y00))
        #box0,1
        x01 = x00
        y01 = random.randint(3,5)
        spots.append((x01,y01))
        #box0,2
        x02 = x00
        y02 = random.randint(6,8)
        spots.append((x02,y02))
        #box1,0
        x10 = random.randint(3,5)
        y10 = y00
        spots.append((x10,y10))
        #box1,1
        x11 = x10
        y11 = y01 
        spots.append((x11,y11))
        #box1,2
        x12 = x10
        y12 = y02
        spots.append((x12,y12))
        #box2,0
        x20 = random.randint(6,8)
        y20 = y00
        spots.append((x20,y20))
        #box2,1
        x21 = x20
        y21 = y01
        spots.append((x21,y21))
        #box2,2
        x22 = x20
        y22 = y02
        spots.append((x22,y22))
        return spots

    def set_position(self,x:int, y:int, val: int) -> bool:
        if not self.__is_position_valid(x,y,val):
            return False
        else:
            self.board[x][y] = val
            return True

    def shift_left(self, to_swap):
        logger.debug(f"shifting left -> {to_swap}")
        # for next three
        #x1,y1
        #x2,y2
        #x3,y3
        #v1 = self._board[]
        pass

    def shift_right(self, to_swap):
        logger.debug(f"shifting right -> {to_swap}")
        pass

    def shift_down(self, to_swap):
        logger.debug(f"shifting down -> {to_swap}")
        pass

    def shift_up(self, to_swap):
        logger.debug(f"shifting up -> {to_swap}")
        pass

    def swap_positions(self,swaps) -> bool:
        logger.debug("swapping positions")
        temp_puzzle = Puzzle(self.board)
        for s in swaps:
            section = int(s[1]/3) + int(s[0]/3)
            v1 = temp_puzzle.board[section][s[0][0]][s[0][1]]
            v2 = temp_puzzle.board[s[1][0]][s[1][1]]
            temp_puzzle.board[s[0][0]][s[0][1]] = v1
            temp_puzzle.board[s[1][0]][s[1][1]] = v2
            if temp_puzzle.is_board_valid():
                self.board = deepcopy(temp_puzzle.board)
                return True

    def swap_position(self,x1:int, y1:int, x2:int, y2:int) -> bool:
        logger.debug("swap position")
        v1 = self.board[x1][y1]
        v2 = self.board[x2][y2]
        self.board[x1][y1] = v2
        self.board[x2][y2] = v1
        logger.debug(f"swapping {x1},{y1}:{v1} with {x2},{y2}:{v2}")
        if self.__is_position_valid(x1,y1,v2) and self.__is_position_valid(x2,y2,v1):
            logger.debug("swapped posoition")
            return True
        else:
            self.board[x1][y1] = v1
            self.board[x2][y2] = v2
            return False

    def is_solved(self) -> bool:
        for y in range(0,9):
            for x in range (0,9):
                if self.board[x][y] == 0:
                    return False
        return True

    def is_board_valid(self) -> bool:
        for xy in range(0,9):
            if not self.__is_position_valid(xy,xy,self.board[xy][xy]):
                return False
        return True

    def __is_position_valid(self,x:int, y:int, val:int) -> bool:
        if val < 1 or val > 9:
            return False
        for xr in range(0,9): 
            if self.board[xr][y] == val: 
                return False
        for yr in range(0,9):
            if self.board[x][yr] == val:
                return False
        for xb in range(0,3):
            for yb in range(0,3):
                if self.board[int(x/3) * 3 + xb][int(y/3) * 3 + yb] == val:
                    return False
        return True

    def __repr__(self):
        return str(self.board)

    def __str__(self):
        data = [] # type: List[str]
        data.append("|" + "-" * 29 + "|")
        for y in range(0,9):
            row = "|"
            for x in range (0,9):
                row += " " + str(self.board[x][y]) + " "
                if (x + 1) % 3 == 0:
                    row += "|"
            data.append(row)
            if (y + 1) % 3 == 0:
                data.append("|" + "-" * 29 + "|")
        return "\n".join(data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    b = Puzzle()
    b.initialize_board()
    print(b)
    b.dummy()
    print(b)
    #b.set_position(0,0,1)
    #b.set_position(0,1,3)
    #b.set_position(8,0,2)
    #b.set_position(0,8,2)
    #print(f"is solved = {b.is_solved()}")