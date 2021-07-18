import random

# Countdown weights letters, so some letters have more chance of appearing than others
vowels = {'a': 15, 'e': 21, 'i': 13, 'o': 13, 'u': 5}
weighted_vowels = [letter for letter in vowels for _ in range(vowels[letter])]

consonants = {'b': 2, 'c': 3, 'd': 6, 'f': 2, 'g': 3, 'h': 2, 'j': 1, 'k': 1, 'l': 5, 'm': 4,
              'n': 7, 'p': 4, 'q': 1, 'r': 9, 's': 9, 't': 9, 'v': 2, 'w': 2, 'x': 1, 'y': 1, 'z': 1}
weighted_consonants = [letter for letter in consonants for _ in range(consonants[letter])]

# Samples the letters
def sampleLetters(n_vowels, n_consonants):
    samples = ([random.choice(weighted_vowels) for _ in range(n_vowels)] +
               [random.choice(weighted_consonants) for _ in range(n_consonants)])
    random.shuffle(samples)
    return samples

print(sampleLetters(4, 5))