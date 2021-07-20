import random
from TrieList import TrieList

#
#
#   GENERATE LETTER SAMPLE
#
#

# Countdown weights letters, so some letters have more chance of appearing than others
vowels = {'A': 15, 'E': 21, 'I': 13, 'O': 13, 'U': 5}
weighted_vowels = [letter for letter in vowels for _ in range(vowels[letter])]

consonants = {'B': 2, 'C': 3, 'D': 6, 'F': 2, 'G': 3, 'H': 2, 'J': 1, 'K': 1, 'L': 5, 'M': 4,
              'N': 7, 'P': 4, 'Q': 1, 'R': 9, 'S': 9, 'T': 9, 'V': 2, 'W': 2, 'X': 1, 'Y': 1, 'Z': 1}
weighted_consonants = [letter for letter in consonants for _ in range(consonants[letter])]


# Samples the letters
def sample_letters(n_vowels, n_consonants):
    samples = ([random.choice(weighted_vowels) for _ in range(n_vowels)] +
               [random.choice(weighted_consonants) for _ in range(n_consonants)])
    random.shuffle(samples)

    # Ensure no more than 9 letters
    return samples[:9]


#
#
#   LOAD TEXT FILE AND ADD ALL WORDS TO TRIE
#
#

trie = TrieList()


def load_words():
    with open('Words_Definitions.txt') as word_file:
        words = word_file.read().splitlines()[2:]

    return words


word_set = load_words()
word_dictionary = {}

for word_definition in word_set:
    (word, definition) = word_definition.split("\t")

    # remove any words with more than 9 letters
    if len(word) < 10:
        word_dictionary[word] = definition

for word in word_dictionary:
    trie.add_word(word)

# trie.print_trie(10,trie.root_node)

#
#
#   Traverse the trie to find compatible words
#
#

samples = sample_letters(3, 6)

print('Samples: ',samples)

words_from_letters = trie.find_words(samples, trie.root_node)

print(words_from_letters)

# order by length
