import random
import string

class Board: 
    def __init__(self, size=4, letters=None): # Create the board.
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
        neighbors = [] # List to store neighbors
        for dr in (-1, 0, 1): # Loop through possible row offsets
            for dc in (-1, 0, 1): # Loop through possible column offsets
                if dr == 0 and dc == 0: # Skip the current cell
                    continue
                nr, nc = r + dr, c + dc # Calculate neighbor coordinates
                if 0 <= nr < self.size and 0 <= nc < self.size:  # Check if within bounds
                    neighbors.append((nr, nc)) # Add valid neighbor to the list
        return neighbors 

# Example usage
if __name__ == '__main__':
    board = Board(size=4) 
    print(board) 
    print(board.get_neighbors(1, 1)) 
    print(board.get_neighbors(0, 0)) 