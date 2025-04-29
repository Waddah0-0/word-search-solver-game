from solver.board    import Board
from solver.trie     import build_trie_from_file
from solver.solver   import find_words
# later, once you have solver code, you’ll import that too

def main():
    # 1) Load the dictionary into your Trie
    # If words.txt lives next to main.py, use the relative path:
    trie = build_trie_from_file('words.txt')
    print("Dictionary loaded!")

    # 2) Create your board
    fixed = [
        ['T','R','E','E'],
        ['A','L','K','S'],
        ['P','O','N','Y'],
        ['F','I','R','E']
    ]
    board = Board(letters=fixed)
    print(board)
    print()

    # 3) Quick sanity‐check on the Trie
    for w in ['TREE', 'BOGGLE', 'XYZ']:
        print(f"{w:7} → in dict? {trie.search(w):5} | starts with BOG? {trie.starts_with('BOG')}")

    # 4) (Later) Pass `board` and `trie` into your solver module to find all words.

    print(board, "\n")

    words = find_words(board, trie)
    print("Words found:")
    print(sorted(words))
if __name__ == '__main__':
    main()
