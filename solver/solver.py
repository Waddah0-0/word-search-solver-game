# solver.py
# aka dfs

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

    def backtrack(r: int, c: int, node, path: set[tuple[int, int]], word: str):  # DFS
        letter = board.grid[r][c]
        if letter not in node.children:
            return

        node = node.children[letter]
        word += letter
        path.add((r, c))

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


def suggest_word(found_words: set[str], already_found: set[str]) -> str:
    """
    Suggest a word from the set of found words that has not yet been found by the user.

    Parameters:
        found_words: set[str] – All valid words found by the AI.
        already_found: set[str] – Words already found by the user.

    Returns:
        A single word suggestion or None if no suggestions are available.
    """
    suggestions = found_words - already_found
    return next(iter(suggestions), None)