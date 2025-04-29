# solver.py
    #aka dfs

from solver.board import Board
from solver.trie import build_trie_from_file, Trie

def find_words(board: Board, trie: Trie, min_length: int = 3) -> set[str]:
    """
    Backtracking search on the Boggle board to find all valid words using a Trie for prefix pruning.

    Parameters:
        board: Board        – your game board
        trie: Trie          – dictionary Trie loaded from words.txt
        min_length: int     – minimum word length to include

    Returns:
        A set of found words.
    """
    found: set[str] = set()
    size = board.size

    def backtrack(r: int, c: int, node, path: set[tuple[int,int]], word: str): # DFS
        letter = board.grid[r][c]
        if letter not in node.children:
            return

        node = node.children[letter]
        word += letter
        path.add((r, c))

        # record valid word
        if node.is_word and len(word) >= min_length:
            found.add(word)

        # explore neighbors
        for nr, nc in board.get_neighbors(r, c):
            if (nr, nc) not in path:
                backtrack(nr, nc, node, path, word)

        # backtrack: remove current cell
        path.remove((r, c))

    # start from every cell
    for i in range(size):
        for j in range(size):
            backtrack(i, j, trie.root, set(), "")

    return found

