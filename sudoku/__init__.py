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

    def shuffle_board(self,n=1):
        """
        shuffles a populated board n-times randomizing layout yielding a valid solved puzzle
        """
        logger.debug(f"shuffling board {n} times")
        swap_positions = list()
        for _ in range(0, n):
            # get two positions in each box to swap making sure positions are unique
            swap1 = self.get_swaps()
            swap2 = self.get_swaps()
            while(len(list(set(swap1) & set(swap2))) > 0):
                logger.debug("reswapping")
                swap2 = self.get_swaps()
            # save the swaps so we can print them
            swap_positions.extend(swap1 + swap2)
            # swap values
            while len(swap1) > 0:
                (x1,y1) = swap1.pop()
                (x2,y2) = swap2.pop()
                v1 = self.board[x1][y1]
                v2 = self.board[x2][y2]
                self.board[x1][y1] = v2
                self.board[x2][y2] = v1
        # print swapped positions
        self.print_swaps(swap_positions)

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
        hidden_positions = list()
        while len(hidden_positions) < n:
            #logger.debug(f"removing {i} of {n}")
            x = random.randint(0,8)
            y = random.randint(0,8)
            if (x,y) not in hidden_positions:
                hidden_positions.append((x,y))
                self.board[x][y] = 0
        self.print_hidden(hidden_positions)

    def solve(self, l=1) -> bool:
        """
        attempts to solve puzzle without guessing
        """
        logger.debug(f"solving puzzle ({l})")
        # get missing coords and capture possible values
        missing_options = list()
        for (x, y) in Puzzle.get_empties(self.board):
            missing_options.append((x, y, Puzzle.get_options(self.board, x, y)))
        # populate the board's missing spots where there is only one possible value
        positions = list()
        for (x,y,options) in missing_options:
            if len(options) == 1:
                #logger.debug(f"setting {x},{y} to {options[0]}")
                self.board[x][y] = options[0]
                positions.append((x,y))
        if len(positions) > 0:
            self.print_fills(positions) 
        # test if bored solved
        if self.is_solved():
            # we're done
            return True
        else:
            if len(positions) > 0:
                return self.solve(l=l)
            else:
                return self.guess(l=l)

    def guess(self, l=1):
        """
        attempts to solve puzzle with guessing
        """
        logger.debug(f"guessing ({l})")
        # get missing coords and capture possible values
        for (x, y) in Puzzle.get_empties(self.board):
            for v in Puzzle.get_options(self.board, x, y):
                test_puzzle = Puzzle(self.board)
                test_puzzle.board[x][y] = v
                test_puzzle.print_guesses([(x,y)])
                if test_puzzle.solve(l=l+1):
                    self.board = Puzzle.copy_board(test_puzzle.board)
                    return True
        return False

    @staticmethod
    def get_empties(board: [[]])-> [(int,int)]:
        empties = list()
        for x in range(0,9):
            for y in range(0,9):
                if board[x][y] == 0:
                    empties.append((x,y))
        #logger.debug(f"empties are {empties}")
        return empties

    @staticmethod
    def get_options(board: [[]], x: int, y:int) -> []:
        """
        for (x,y) that should be empty, return a list of possible values
        """
        xs = Puzzle.get_missing_x(board, y)
        #logger.debug(f"missing x's = {xs}")

        ys = Puzzle.get_missing_y(board, x)
        #logger.debug(f"missing y's = {ys}")

        vs = Puzzle.get_missing_v(board, int(x/3), int(y/3))
        #logger.debug(f"missing v's = {vs}")

        options = list(set(xs) & set(ys) & set(vs))
        #logger.debug(f"missing options for {x},{y} = {options}")

        return options

    @staticmethod
    def get_missing_x(board: [[]], y: int) -> []:
        """
        find values missing along x axis for given y value
        """
        xs = [board[x][y] for x in range(0,9)]
        return list(set(Puzzle.vals) - set(xs))

    @staticmethod
    def get_missing_y(board: [[]], x: int) -> []:
        """
        find values missing along y axis for given x value
        """
        ys = [board[x][y] for y in range(0,9)]
        return list(set(Puzzle.vals) - set(ys))

    @staticmethod
    def get_missing_v(board: [[]],box_x: int, box_y:int) -> []:
        """
        find values missing within given box(x,y)
        """
        vs = list()
        for x in range(0,3):
            for y in range(0,3):
                vs.append(board[box_x * 3 + x][box_y * 3 + y])
        return list(set(Puzzle.vals) - set(vs))

    def __repr__(self):
        return str(self.board)

    def __str__(self):
        return self.draw_positions(Fore.WHITE, [])

    def print_board(self):
        logger.debug("print board")
        print(self.draw_positions(Fore.WHITE, []))

    def print_swaps(self, swaps: []):
        logger.debug("print swaps")
        print(self.draw_positions(Fore.GREEN, swaps))

    def print_hidden(self, hidden: []):
        logger.debug("print hidden")
        print(self.draw_positions(Fore.MAGENTA, hidden))

    def print_guesses(self, guesses: []):
        logger.debug("print guesses")
        print(self.draw_positions(Fore.RED, guesses))

    def print_fills(self, fills: []):
        logger.debug("print fills")
        print(self.draw_positions(Fore.CYAN, fills))

    def draw_positions(self, mod_color, positions) -> str:
        data = list()
        data.append("|" + "-" * 29 + "|")
        for y in range(8,-1,-1):
            row = "|"
            for x in range (0,9):
                color = mod_color if (x,y) in positions else Fore.WHITE
                row += " " + color + str(self.board[x][y]) + Fore.RESET + " "
                if (x + 1) % 3 == 0:
                    row += "|"
            data.append(row)
            if y % 3 == 0:
                data.append("|" + "-" * 29 + "|")
        return "\n".join(data)


if __name__ == "__main__":
    colorama.init()
    logging.basicConfig(level=logging.DEBUG)
    b = Puzzle()
    b.initialize_board()
    b.populate_board()
    print(b)
    print(b.is_solved())
    b.shuffle_board(n=18)
    print(b.is_solved())
    b.hide_values(n=50)
    print(b.solve())
    #b.board[0][8] = 9
    #print(b)
    #print(b.is_solved())
    #b.set_position(0,0,1)
    #b.set_position(0,1,3)
    #b.set_position(8,0,2)
    #b.set_position(0,8,2)
    #print(f"is solved = {b.is_solved()}")