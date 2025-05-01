import random
import string

class Board:
    def __init__(self, size=4, letters=None):
        """
        Create a size×size board.
        If `letters` is provided, it must be a list of lists of single chars.
        Otherwise we’ll fill with random uppercase English letters.
        """
        self.size = size
        if letters:
            self.grid = letters
        else:
            self.grid = [
                [random.choice(string.ascii_uppercase) for _ in range(size)]
                for _ in range(size) 
            ]

    def __str__(self):
        # Nice ASCII-art printing of the board
        rows = [" ".join(row) for row in self.grid]
        return "\n".join(rows)

    def get_neighbors(self, r, c):
        """
        Return a list of (nr, nc) for all valid neighbors of cell (r,c).
        """
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size: 
                    neighbors.append((nr, nc))
        return neighbors 
