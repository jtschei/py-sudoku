import unittest
import sudoku as s

class TestSudoku(unittest.TestCase):

    def test_solve(self):
        p = s.Puzzle()
        v: int = 0
        for x in range(0,9):
            for y in range(0,9):
                if (x % 3 == 0 and y == 0):
                    v = int(x/3)
                p.board[x][y] = v % 9 + 1
                if (not (x == 8 and y == 8)):
                    self.assertFalse(p.is_solved())
                v = v+1
            v = v + 3
        print()
        print(p)
        self.assertTrue(p.is_solved())


if __name__ == '__main__':
    unittest.main()