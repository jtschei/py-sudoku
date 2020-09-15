from colorama import Fore, Back, Style
import colorama
import logging
import random
import itertools

logger = logging.getLogger()


class Puzzle:

    vals = [1,2,3,4,5,6,7,8,9]

    def __init__(self, board: [[]] = None):
        logger.debug("creating puzzle")
        if board is None:
            self.board = Puzzle.build_blank_board()
        else:
            self.board = Puzzle.copy_board(board)

    @staticmethod
    def build_blank_board() -> [[]]:
        logger.debug("building blank board")
        return [[0] * 9 for i in range(9)]

    @staticmethod
    def copy_board(orig_board: [[]]) -> [[]]:
        logger.debug("copying board")
        copy_board = Puzzle.build_blank_board()
        for x in range(0,9):
            for y in range(0,9):
                copy_board[x][y] = orig_board[x][y]
        return copy_board

    def initialize_board(self):
        """
        reset board to all 0's
        """
        logger.debug("initializing board")
        for x in range(0,9):
            for y in range(0,9):
                self.board[x][y] = 0

    def populate_board(self):
        """
        populate a board with values yielding a valid solved puzzle
        """
        logger.debug("populating board")
        v: int = 0
        for x in range(0,9):
            for y in range(0,9):
                if x % 3 == 0 and y == 0:
                    v = int(x/3)
                self.board[x][y] = v % 9 + 1
                v = v+1
            v = v + 3

    def is_solved(self) -> bool:
        """
        return true if the puzzle is complete and valid
        """
        logger.debug("testing if puzzle is solved")
        # get checklist for values 1-9 with all entries initialized as False 
        def get_checklist():
            return [False for x in range(0,9)]
        # each row has 1-9
        for y in range(0,9):
            checklist = get_checklist()
            for x in range(0,9):
                val = self.board[x][y] - 1
                if checklist[val]:
                    return False
                checklist[val] = True
            if False in checklist:
                return False
        # each column has 1-9
        for x in range(0,9):
            checklist = get_checklist()
            for y in range(0,9):
                val = self.board[x][y] - 1
                if checklist[val]:
                    return False
                checklist[val] = True
            if False in checklist:
                return False
        # each box has 1-9
        for bx in range(0,3):
            for by in range(0,3):
                checklist = get_checklist()
                for x in range(bx*3,(bx*3)+3):
                    for y in range((by*3),(by*3)+3):
                        val = self.board[x][y] - 1
                        if checklist[val]:
                            return False
                        checklist[val] = True
                if False in checklist:
                    return False
        # valid
        return True

    def shuffle_board(self):
        """
        shuffles a populated board randomizing layout yielding a valid solved puzzle
        """
        logger.debug("shuffling board")
        # get two positions in each box to swap making sure positions are unique
        swap1 = self.get_swaps()
        swap2 = self.get_swaps()
        while(len(list(set(swap1) & set(swap2))) > 0):
            logger.debug("reswapping")
            swap2 = self.get_swaps()
        # swap values
        self.print_swaps(swap1 + swap2)
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
        # pick a random position in first box and to list of spots
        x00=random.randint(0,2)
        y00=random.randint(0,2)
        spots.append((x00,y00))
        # find the position where value of prior position matches in remainder
        # boxes and add to list of spts
        for x in range(0,9):
            for y in range(0,9):
                if x < 3 and y < 3:
                    continue
                if self.board[x][y] == self.board[x00][y00]:
                    spots.append((x,y))
        return spots

    def hide_values(self, n=9):
        for i in range(n):
            logger.debug(f"removing {i} of {n}")
            x = random.randint(0,8)
            y = random.randint(0,8)
            self.board[x][y] = 0

    def solve(self) -> bool:
        for x in range(0,9):
            for y in range(0,9):
                if self.board[x][y] == 0:
                    p = Puzzle.try_solve(self.board, x, y)
                    if p is not None:
                        self.board = Puzzle.copy_board(p.board)
                        print(self)
                        logger.info("solved")
                        return True
        return False

    @staticmethod
    def get_next_empty(board: [[]], px: int, py:int) -> (bool,int,int):
        for x in range(0,9):
            for y in range(0,9):
                if x < px or y < py:
                    continue
                if board[x][y] == 0:
                    return (True,x,y)
        return (False, None, None)

    @staticmethod
    def try_solve(board: [[]], x: int, y:int):
        logger.debug(f"solving board for {x},{y}")
        p = Puzzle(board)
        print(p)
        xs = p.get_missing_x(y)
        ys = p.get_missing_y(x)
        vs = p.get_missing_v(int(x/3),int(y/3))
        os = list(set(xs) & set(ys) & set(vs))

        logger.debug(f"missing x's = {xs}")
        logger.debug(f"missing y's = {ys}")
        logger.debug(f"missing v's = {vs}")
        logger.debug(f"missing o's = {os}")

        for o in os:
            p.board[x][y] = o
            if p.is_solved():
                return p
            else:
                b, nx, ny = Puzzle.get_next_empty(p.board, x, y)
                if b:
                    return Puzzle.try_solve(p.board, nx, ny)

    def get_missing_x(self, y: int) -> []:
        xs = [self.board[x][y] for x in range(0,9)]
        return list(set(Puzzle.vals) - set(xs))

    def get_missing_y(self, x: int) -> []:
        ys = [self.board[x][y] for y in range(0,9)]
        return list(set(Puzzle.vals) - set(ys))

    def get_missing_v(self,box_x: int, box_y:int) -> []:
        vs = list()
        for x in range(0,3):
            for y in range(0,3):
                vs.append(self.board[box_x * 3 + x][box_y * 3 + y])
        return list(set(Puzzle.vals) - set(vs))

    def __repr__(self):
        return str(self.board)

    def __str__(self):
        data = [] # type: List[str]
        data.append("|" + "-" * 29 + "|")
        for y in range(8,-1,-1):
            row = "|"
            for x in range (0,9):
                row += " " + str(self.board[x][y]) + " "
                if (x + 1) % 3 == 0:
                    row += "|"
            data.append(row)
            if y % 3 == 0:
                data.append("|" + "-" * 29 + "|")
        return "\n".join(data)

    def print_board(self):
        return str(self)

    def print_swaps(self, swaps):
        logger.debug("print swaps")
        data = [] # type: List[str]
        data.append("|" + "-" * 29 + "|")
        for y in range(8,-1,-1):
            row = "|"
            for x in range (0,9):
                color = Fore.GREEN if (x,y) in swaps else Fore.WHITE
                row += " " + color + str(self.board[x][y]) + Fore.RESET + " "
                if (x + 1) % 3 == 0:
                    row += "|"
            data.append(row)
            if y % 3 == 0:
                data.append("|" + "-" * 29 + "|")
        print("\n".join(data))


if __name__ == "__main__":
    colorama.init()
    logging.basicConfig(level=logging.DEBUG)
    b = Puzzle()
    b.initialize_board()
    b.populate_board()
    print(b.is_solved())
    print(b)
    for x in range(0,10):
        b.shuffle_board()
        print(b.is_solved())
    print(b)
    b.hide_values()
    print(b)
    b.solve()
    #b.board[0][8] = 9
    #print(b)
    #print(b.is_solved())
    #b.set_position(0,0,1)
    #b.set_position(0,1,3)
    #b.set_position(8,0,2)
    #b.set_position(0,8,2)
    #print(f"is solved = {b.is_solved()}")