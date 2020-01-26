class Board:
    def __init__(self):
        self.reset_board()

    def reset_board(self):
        self._board = [[0] * 9 for i in range(9)]

    def __repr__(self):
        return str(self._board)

    def __str__(self):
        header : str = "/" + "-" * 35 + "\\" 
        data : str = "\n".join(map(lambda y: "|" + "|".join(map(lambda n : f" {n} ", self._board[y])) + "|",range(9)))
        footer : str = "\\" + "-" * 35 + "/" 
        return "\n".join((header,data,footer))

class Row:
    def __init__(self):
        pass


if __name__ == "__main__":
    b = Board()
    print(b)