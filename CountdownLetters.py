from typing import List
from typing import Dict
import random
from TrieList import TrieList

#
#
#   GENERATE LETTER SAMPLE
#
#

# Countdown weights letters, so some letters have more chance of appearing than others
vowels: Dict[str,int] = {'A': 15, 'E': 21, 'I': 13, 'O': 13, 'U': 5}
weighted_vowels: List[str] = [letter for letter in vowels for _ in range(vowels[letter])]

consonants: Dict[str,int] = {'B': 2, 'C': 3, 'D': 6, 'F': 2, 'G': 3, 'H': 2, 'J': 1, 'K': 1, 'L': 5, 'M': 4,
              'N': 7, 'P': 4, 'Q': 1, 'R': 9, 'S': 9, 'T': 9, 'V': 2, 'W': 2, 'X': 1, 'Y': 1, 'Z': 1}
weighted_consonants: List[str] = [letter for letter in consonants for _ in range(consonants[letter])]


# Samples the letters
def sample_letters(n_vowels, n_consonants) -> List[str]:

    samples: List[str] = ([random.choice(weighted_vowels) for _ in range(n_vowels)] +
               [random.choice(weighted_consonants) for _ in range(n_consonants)])

    random.shuffle(samples)

    # Ensure no more than 9 letters
    return samples[:9]


#
#
#   LOAD TEXT FILE AND ADD ALL WORDS TO TRIE
#
#

# Generate new trie
trie = TrieList()


# Split lines of text file
def load_words() -> List[str]:
    with open('Words_Definitions.txt') as word_file:
        words: List[str] = word_file.read().splitlines()[2:]

    return words


word_set: List[str] = load_words()

# Dictionary of Word:Definition to populate
word_dictionary: Dict[str,str] = {}

# Split each line and populate word_dictionary
for word_definition in word_set:

    # Split each line to word and definition
    (word, definition) = word_definition.split("\t")

    # Only include words with 9 letters or less
    if len(word) < 10:
        word_dictionary[word] = definition

# Add words to trie
for word in word_dictionary:
    trie.add_word(word)


#
#
#   Traverse the trie to find compatible words
#
#

def print_words(letters: [str]):
    print('Letters: ', letters, "\n")

    # Find words from the trie and order them by length
    words_from_letters: List[str] = trie.find_words(letters, trie.root_node)
    words_from_letters.sort(key=len, reverse=True)

    # Only show words with max length, printing the word and definition
    max_length: int = len(words_from_letters[0])

    for word in words_from_letters:
        if len(word) == max_length:
            print(word)
            print(word_dictionary[word], "\n")
        else:
            break


#
#
# User input
#
#

while True:
    mode: str = ''

    while mode != 'R' and mode != 'C' and mode != 'X':
        mode = input("Random [R], Chosen [C], Exit [X]\n").upper()

    # Random selected, so prompt the amount of vowels/consonants
    if mode == 'R':

        n_vowels: int = -1

        while not 0 <= n_vowels < 10:

            try:
                n_vowels = int(input('How many vowels? (0 to 9) \n'))
                if not 0 <= n_vowels < 10:
                    print("Enter an integer between 0 and 9\n")
            except ValueError:
                print("Enter an integer between 0 and 9\n")

        # Sample 9 letters
        n_consonants: int = 9 - n_vowels
        print(n_vowels, ' vowels, ', n_consonants, ' consonants\n')
        samples: List[str] = sample_letters(n_vowels, n_consonants)
        print_words(samples)

    elif mode == 'C':
        letters: List[str] = []

        # Ask user to choose 9 letters
        while len(letters) < 9:
            letter_prompt = input("Letter " + str(len(letters) + 1) + ":\n").upper()
            if letter_prompt in vowels or letter_prompt in consonants:
                letters.append(letter_prompt)
            else:
                print("Invalid")

        print_words(letters)

    # Exit
    elif mode == 'X':
        break
