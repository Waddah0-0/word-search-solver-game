class TrieNode: # A single node in the Trie
    def __init__(self): # Initialize a TrieNode with an empty dictionary for children and a boolean for word end
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False

class Trie: # A Trie data structure for storing words
    def __init__(self): # Initialize the Trie with a root node
        self.root = TrieNode()

    def insert(self, word: str) -> None: # Insert a word into the Trie
        """
        Insert a word into the trie.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word: str) -> bool: # exact word search
        """
        Return True if the exact word exists in the trie.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

    def starts_with(self, prefix: str) -> bool: # prefix search
        """
        Return True if there is any word in the trie that starts with the given prefix.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def build_trie_from_file(filepath: str) -> Trie: # Build a Trie from a file containing newline-separated words
    """
    Build a Trie from a newline-separated word list file.
    Words are normalized to uppercase and stripped of whitespace.
    """
    trie = Trie()
    with open(filepath, 'r') as f:
        for line in f:
            word = line.strip().upper()
            if word:
                trie.insert(word)
    return trie


# Example usage
if __name__ == '__main__':
    # Adjust the path to your word list file
    trie = build_trie_from_file('words.txt')
    print("Loaded trie.")
    # Quick checks
    sample = ['TREE', 'TRICK', 'XYZ']
    for w in sample:
        print(f"{w}: in dictionary? {trie.search(w)} | starts with 'T'? {trie.starts_with('T')}")
