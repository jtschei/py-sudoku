class Puzzle:
    def __init__(self):
        self.reset_board()

    def reset_board(self):
        self._board = [[0] * 9 for i in range(9)]

    def set_position(self,x:int, y:int, val: int) -> bool:
        if (not self._is_position_valid(x,y,val)):
            return False
        else:
            self._board[x][y] = val
            return True

    def is_solved(self) -> bool:
        for y in range(0,9):
            for x in range (0,9):
                if (self._board[x][y] == 0):
                    return False
        return True

    def _is_position_valid(self,x:int, y:int, val:int) -> bool:
        if (val < 1 or val > 9):
            return False
        for xr in range(0,9): 
            if (self._board[xr][y] == val): 
                return False
        for yr in range(0,9):
            if (self._board[x][yr] == val):
                return False
        for xb in range(0,3):
            for yb in range(0,3):
                if (self._board[int(x/3) * 3 + xb][int(y/3) * 3 + yb] == val):
                    return False
        return True

    def __repr__(self):
        return str(self._board)

    def __str__(self):
        data = [] # type: List[str]
        data.append("|" + "-" * 29 + "|")
        for y in range(0,9):
            row = "|"
            for x in range (0,9):
                row += " " + str(self._board[x][y]) + " "
                if ((x + 1) % 3 == 0):
                    row += "|"
            data.append(row)
            if ((y + 1) % 3 == 0):
                data.append("|" + "-" * 29 + "|")
        return "\n".join(data)

if __name__ == "__main__":
    b = Puzzle()
    b.set_position(0,0,1)
    b.set_position(0,1,3)
    b.set_position(8,0,2)
    b.set_position(0,8,2)
    print(b)
    print(f"is solved = {b.is_solved()}")