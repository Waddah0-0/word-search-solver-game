import random
import string

class Board: 
    def __init__(self, size=4, letters=None): # Create the board.
        """
        Create a size×size board.
        If `letters` is provided, it must be a list of lists of single chars.
        Otherwise we’ll fill with random uppercase English letters.
        """
        self.size = size # Size of the board
        if letters: # If letters are provided, use them to create the board
            self.grid = letters # Create the grid with provided letters
        else: # Otherwise, fill the board with random uppercase letters
            self.grid = [ 
                [random.choice(string.ascii_uppercase) for _ in range(size)]
                for _ in range(size) 
            ] # Create a grid of random letters

    def __str__(self): ## String representation of the board
        # Nice ASCII-art printing of the board
        rows = [" ".join(row) for row in self.grid]
        return "\n".join(rows)

    def get_neighbors(self, r, c): # Get neighbors of a cell
        """
        Return a list of (nr, nc) for all valid neighbors of cell (r,c).
        """
        neighbors = [] # List to store neighbors
        for dr in (-1, 0, 1): # Loop through possible row offsets
            for dc in (-1, 0, 1): # Loop through possible column offsets
                if dr == 0 and dc == 0: # Skip the current cell
                    continue
                nr, nc = r + dr, c + dc # Calculate neighbor coordinates
                if 0 <= nr < self.size and 0 <= nc < self.size:  # Check if within bounds
                    neighbors.append((nr, nc)) # Add valid neighbor to the list
        return neighbors 
