# solver.py
# aka dfs

from solver.board import Board 
from solver.trie import Trie

def find_words(board: Board, trie: Trie, min_length: int = 3) -> set[str]:
    found: set[str] = set() # Set to store found words
    size = board.size # Size of the board

    def backtrack(r: int, c: int, node, path: set[tuple[int, int]], word: str):  # DFS 
        letter = board.grid[r][c] # Current letter
        if letter not in node.children:     # If letter not in Trie, stop search
            return

        node = node.children[letter] # Move to the next Trie node
        word += letter # Add letter to current word
        path.add((r, c)) # Add current cell to path

        # Record valid word
        if node.is_word and len(word) >= min_length:
            found.add(word)

        # Explore neighbors
        for nr, nc in board.get_neighbors(r, c):
            if (nr, nc) not in path:
                backtrack(nr, nc, node, path, word)

        # Backtrack: remove current cell
        path.remove((r, c))

    # Start from every cell
    for i in range(size):
        for j in range(size):
            backtrack(i, j, trie.root, set(), "")

    return found


def suggest_word(found_words: set[str], already_found: set[str]) -> str:    # method to suggest a word
    suggestions = found_words - already_found # Get words not already found
    return next(iter(suggestions), None) # Return first suggestion or None if empty