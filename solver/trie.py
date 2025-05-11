class TrieNode: # A single node in the Trie
    def __init__(self): # Initialize a TrieNode with an empty dictionary for children and a boolean for word end
        self.children: dict[str, TrieNode] = {} # Dictionary to store child nodes
        self.is_word: bool = False

class Trie: # A Trie data structure for storing words
    def __init__(self): # Initialize the Trie with a root node
        self.root = TrieNode()

    def insert(self, word: str) -> None: # Insert a word into the Trie
        node = self.root
        for char in word:
            if char not in node.children: 
                node.children[char] = TrieNode()  
            node = node.children[char]   
        node.is_word = True 

    def search(self, word: str) -> bool: # exact word search
        node = self.root # Start from the root node
        for char in word: # Loop through each character in the word
            if char not in node.children: # If character not found in children, word doesn't exist
                return False # Word not found
            node = node.children[char] # Move to the next node
        return node.is_word

    def starts_with(self, prefix: str) -> bool: # prefix search
        node = self.root # Start from the root node
        for char in prefix: # Loop through each character in the prefix
            if char not in node.children: # If character not found in children, no word starts with this prefix
                return False
            node = node.children[char] # Move to the next node
        return True 


def build_trie_from_file(filepath: str) -> Trie: 
    trie = Trie() # Create a new Trie instance
    with open(filepath, 'r') as f:  
        for line in f: # Read each line from the file
            word = line.strip().upper() # Normalize the word to uppercase and strip whitespace
            if word: # If the word is not empty, insert it into the Trie
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
        print(f"{w}: in dictionary? {trie.search(w)} | starts with 'T'? {trie.starts_with('T')} ")
