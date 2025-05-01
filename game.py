import time
from solver.board import Board
from solver.trie import build_trie_from_file
from solver.solver import find_words

# Scoring rules for Boggle (example):
# 3-4 letters: 1 point
# 5 letters: 2 points
# 6 letters: 3 points
# 7 letters: 5 points
# 8+ letters: 11 points
SCORING = { 
    3: 1,
    4: 1,
    5: 2,
    6: 3,
    7: 5,
}


def score_word(word: str) -> int: # Calculate score for a word based on its length
    return SCORING.get(len(word), 11 if len(word) >= 8 else 0)


def play_game(board_size: int = 4, time_limit: int = 180): # Main game loop
    # 1) Setup
    board = Board(size=board_size)
    trie = build_trie_from_file('words.txt')
    all_valid = find_words(board, trie)

    print("Welcome to Boggle!")
    print(f"You have {time_limit} seconds to find as many words as you can.")
    print("Board:")
    print(board)
    print()

    # 2) User input phase
    start = time.time()
    entered = set() # Set to store entered words
    while time.time() - start < time_limit:
        remaining = int(time_limit - (time.time() - start))
        guess = input(f"{remaining}s left, enter word (or just Enter to finish): ").strip().upper()
        if not guess:
            break
        if guess in entered:
            print("Already entered.")
        elif guess in all_valid:
            print(f"Good! +{score_word(guess)} points.")
            entered.add(guess)
        else:
            print("Not valid.")

    # 3) Scoring
    total = sum(score_word(w) for w in entered)
    print(f"\nTime's up! You found {len(entered)} words for {total} points.")

    # 4) Reveal solution
    print("\nAll possible words:")
    for w in sorted(all_valid):
        marker = "*" if w in entered else " "
        print(f"{marker} {w} ({score_word(w)})")


if __name__ == '__main__':
    play_game()
