class TrieNode:

    def __init__(self, letter: str, complete_word: bool):
        # Letter of current node
        self.letter: str = letter

        # Children of this node
        self.children: [TrieNode] = []

        # If current node is a complete_word node
        self.complete_word: bool = complete_word


class TrieList:

    def __init__(self):
        self.root_node: TrieNode = TrieNode('', False)

    #
    #
    #   ADD WORD TO TREE
    #
    #

    def add_word(self, word: str):

        # Start at the root node
        node: TrieNode = self.root_node

        # Traversal will be the length of the word at most
        for letter in word:

            letter_found: bool = False

            # Check all children of node for the letter
            for child in node.children:

                # Letter is in children so traverse 1 deeper and go to next letter
                if child.letter == letter:
                    node = child
                    letter_found = True
                    break

            # Letter is not in children
            if not letter_found:
                # Make a new child node and assign it the letter
                child_node: TrieNode = TrieNode(letter, False)
                node.children.append(child_node)

                # Move to the child node
                node = child_node

        # Node after fully iterating loop has the last letter, so set complete_word to True
        node.complete_word = True

    #
    #
    #   FIND LONGEST WORDS (AND PROVIDE DEFINITIONS)
    #
    #

    # Collects all words that can be made from the letters
    def find_words(self, letters: [str], node: TrieNode, prefix: str = '') -> [str]:

        valid_words = []

        if node.complete_word:
            valid_words.append(prefix)

        # Check every node for matching letters
        for child in node.children:
            # Set to avoid traversing multiple times for the same letter
            for letter in set(letters):
                if letter == child.letter:
                    # Remove 1st element of the letter from letters
                    letters_copy = letters.copy()
                    letters_copy.remove(letter)
                    valid_words += self.find_words(letters_copy, child, prefix + child.letter)

        return valid_words

    #
    #
    #   PRINT TREE (to n rows)
    #
    #

    def print_trie(self, n: int, node: TrieNode, prefix: str = ''):

        if n == 0:
            return

        prefix += node.letter

        midpoint: int = len(node.children) // 2

        for index, child in enumerate(node.children):
            if index <= midpoint:
                # print above a level to the right
                self.print_trie(n - 1, child, prefix)

        # print current node at level
        if node.complete_word:
            print(" " * 3 * n, '[', prefix, ']')
        else:
            print(" " * 3 * n, prefix)

        for index, child in enumerate(node.children):
            if index > midpoint:
                # print the rest below a level to the right
                self.print_trie(n - 1, child, prefix)
