from colorama import Fore, Back, Style
import colorama
import logging
import random
import itertools

logger = logging.getLogger()

class Puzzle:
    def __init__(self, board: [[]] = None):
        logger.debug("creating puzzle")
        if board is None:
            self.board = Puzzle.build_blank_board()
        else:
            self.board = Puzzle.copy_board(board)

    @staticmethod
    def build_blank_board() -> [[]]:
        logger.debug("building initialized board")
        return [[0] * 9 for i in range(9)]

    @staticmethod
    def copy_board(orig_board: [[]]) -> [[]]:
        logger.debug("copying board")
        copy_board = [[0] * 9 for i in range(9)]
        for x in range(0,9):
            for y in range(0,9):
                copy_board[x][y] = orig_board[x][y]
        return copy_board

    def initialize_board(self):
        logger.debug("initializing board")
        for x in range(0,9):
            for y in range(0,9):
                self.board[x][y] = 0

    def populate_board(self):
        logger.debug("populating board")
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
        # get two positions in each box to swap making sure positions are unique
        swap1 = self.get_swaps()
        swap2 = self.get_swaps()
        while(len(list(set(swap1) & set(swap2))) > 0):
            logger.debug("reswapping")
            swap2 = self.get_swaps()
        swaps = list()
        for s in swap1:
            swaps.append(s)
        for s in swap2:
            swaps.append(s)
        self.print_swaps(swaps)
        # swap values
        while len(swap1) > 0:
            (x1,y1) = swap1.pop()
            (x2,y2) = swap2.pop()
            v1 = self.board[x1][y1]
            v2 = self.board[x2][y2]
            self.board[x1][y1] = v2
            self.board[x2][y2] = v1


    def get_swaps(self):
        """
        pick two positions in box0,0
        identify the positions in the other boxes for corresponding values
        the values in the two positions can be switched in each box
        """
        spots=list()
        x00=random.randint(0,2)
        y00=random.randint(0,2)
        spots.append((x00,y00))
        for x in range(0,9):
            for y in range(0,9):
                if x < 3 and y < 3:
                    continue
                if self.board[x][y] == self.board[x00][y00]:
                    spots.append((x,y))
        return spots

    def set_position(self,x:int, y:int, val: int) -> bool:
        if not self.__is_position_valid(x,y,val):
            return False
        else:
            self.board[x][y] = val
            return True

    def swap_position(self,x1:int, y1:int, x2:int, y2:int) -> bool:
        # TODO - broken
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
        # TODO - broken
        for y in range(0,9):
            for x in range (0,9):
                if self.board[x][y] == 0:
                    return False
        return True

    def is_board_valid(self) -> bool:
        # TODO - broken
        for xy in range(0,9):
            if not self.__is_position_valid(xy,xy,self.board[xy][xy]):
                return False
        return True

    def __is_position_valid(self,x:int, y:int, val:int) -> bool:
        # TODO - broken
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

    def print_swaps(self, swaps):
        logger.debug("print swaps")
        data = [] # type: List[str]
        data.append("|" + "-" * 29 + "|")
        for y in range(0,9):
            row = "|"
            for x in range (0,9):
                color = Fore.GREEN if (x,y) in swaps else Fore.WHITE
                row += " " + color + str(self.board[x][y]) + Fore.RESET + " "
                if (x + 1) % 3 == 0:
                    row += "|"
            data.append(row)
            if (y + 1) % 3 == 0:
                data.append("|" + "-" * 29 + "|")
        print("\n".join(data))
        


if __name__ == "__main__":
    colorama.init()
    logging.basicConfig(level=logging.DEBUG)
    b = Puzzle()
    b.initialize_board()
    b.populate_board()
    print(b)
    for x in range(0,9):
        b.shuffle_board()
    print(b)
    #b.set_position(0,0,1)
    #b.set_position(0,1,3)
    #b.set_position(8,0,2)
    #b.set_position(0,8,2)
    #print(f"is solved = {b.is_solved()}")