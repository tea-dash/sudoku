class SudokuGrid:
    def __init__(self, board=None):
        # board: 9×9 list of ints (0 = empty)
        self.board = board or [[0]*9 for _ in range(9)]
        # precompute row/col/box sets
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]
        self._init_sets()

    def _init_sets(self):
        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                if val:
                    self.rows[r].add(val)
                    self.cols[c].add(val)
                    self.boxes[(r//3)*3 + c//3].add(val)

    def is_valid(self, r, c, val):
        """Check if placing val at position (r, c) is valid."""
        b = (r//3)*3 + c//3
        return (val not in self.rows[r] and 
                val not in self.cols[c] and 
                val not in self.boxes[b])

    def place(self, r, c, val):
        """Place val at position (r, c) and update sets."""
        self.board[r][c] = val
        self.rows[r].add(val)
        self.cols[c].add(val)
        self.boxes[(r//3)*3 + c//3].add(val)

    def remove(self, r, c, val):
        """Remove val from position (r, c) and update sets."""
        self.board[r][c] = 0
        self.rows[r].remove(val)
        self.cols[c].remove(val)
        self.boxes[(r//3)*3 + c//3].remove(val)
        
    def is_complete(self):
        """Check if the grid is completely filled."""
        return all(self.board[r][c] != 0 for r in range(9) for c in range(9))
        
    def copy(self):
        """Create a deep copy of the grid."""
        return SudokuGrid([row[:] for row in self.board])
