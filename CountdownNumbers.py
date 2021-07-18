import random

#
#
# NUMBER GENERATION
#
#

bigs = [100, 75, 50, 25, 10]
smalls = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Generates numbers based on an amount of big / small
def sampleNumbers(big, small):
    samples = [random.choice(bigs) for _ in range(big)] + [random.choice(smalls) for _ in range(small)]
    random.shuffle(samples)
    return samples


# Target number to aim for
def target():
    return random.randint(100, 999)


#
#
# Print out results
#
#

samples = sampleNumbers(2, 4)

for i in samples:
    print(i)

print("TARGET: ", target())

#
#
# BRUTE FORCE !!
#
#


#
#
# SMARTER...
#
#
