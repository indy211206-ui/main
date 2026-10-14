from math import sqrt

class Sudoku(object):
    def __init__(self, data):
        self.data = data
    def is_valid(self):
        board = self.data
        n = len(board)
        k = int(sqrt(len(board)))
        valid = set(range(1, n + 1))
        if any(len(r) != n for r in board) or k*k != n or n == 0:
            return False
        for c in range(n):
            row = set(board[c])
            col = set(board[r][c] for r in range(n))
            if row != valid or col != valid:
                return False
        for sr in range(0, n, k):
            for sc in range(0, n, k):
                square = set()
                for i in range(k):
                    for j in range(k):
                        square.add(board[sr + i][sc + j])
                if square != valid:
                    return False
        return True
