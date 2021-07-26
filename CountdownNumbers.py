from typing import List
import random

#
#
# NUMBER GENERATION
#
#

bigs: List[int] = [100, 75, 50, 25]
smalls: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# Generates numbers based on an amount of big / small
def sample_numbers(big, small) -> List[int]:
    samples: List[int] = [random.choice(bigs) for _ in range(big)] + [random.choice(smalls) for _ in range(small)]
    random.shuffle(samples)
    return samples


# Target number to aim for
def target() -> int:
    return random.randint(101, 999)


#
#
# Print out results
#
#

samples: List[int] = sample_numbers(2, 4)

for i in samples:
    print(i)

target_num = target()
print("TARGET: ", target_num)


#
#
# Algorithm for solving numbers
#
#

class NumbersSolver:

    def __init__(self):
        self.best: int = 0
        self.counter: int = 0

    # See if the number is the closest to the target
    def compare_to_best(self, n: int, target: int):
        if abs(target - n) < abs(target - self.best):
            self.best = n

    # Custom function similar to itertools.combinations(xs,2), but also
    # yields the indexes of each combination from within the original list
    def custom_combo(self, xs: List):
        for i, xi in enumerate(xs):
            for j, xj in enumerate(xs):
                if i < j:
                    yield (xi, xj, i, j)

    # Get list of all values that can be made from 2 integers
    def operation_results(self, a: int, b: int) -> List[int]:

        # Order doesn't matter for addition and multiplication
        add: int = a + b
        mult: int = a * b

        # Order matters for subtraction and division
        (bigger, smaller) = (a, b) if a > b else (b, a)

        sub: int = bigger - smaller

        self.counter += 3

        # Division is invalid if divisor is 0 or it doesn't result in an integer
        if smaller == 0 or bigger % smaller != 0:
            return [add, sub, mult]

        div: int = bigger // smaller
        self.counter += 1

        return [add, sub, mult, div]

    # All operation_results between 2 lists
    def list_operations(self, alist: List[int], blist: List[int]) -> List[int]:

        final_list: List[int] = []

        for a in alist:
            for b in blist:
                final_list += self.operation_results(a, b)

        return final_list

    # Set best to default and set the numbers to the form [[x],[y],[z] ... ]
    def initialise(self, numbers: List[int], target: int) -> List[List[int]]:

        # set best to 0
        self.best = 0

        # Using all of the numbers on their own
        for n in numbers:
            self.compare_to_best(n, target)

        # return numbers as a list of lists [[x],[y],[z] ... ]
        return [[n] for n in numbers]

    # Numbers must be supplied in the form [[x],[y],[z] ... ] to simplify the algorithm.
    # Since list_operations returns a list, the values in numbers must be lists too.
    def calculate_results(self, numbers: List[List[int]], target: int):

        if len(numbers) > 1:
            # Get all pairs of lists within the list
            for xi, xj, i, j in self.custom_combo(numbers):

                # Results of all possible operations between 2 of the lists
                combo_result = self.list_operations(xi, xj)

                # Match every int in every combo against the target and update best
                for n in combo_result:
                    self.compare_to_best(n, target)

                # Get a new numbers_list with the combo_result replacing its inputs
                new_numbers_list = numbers.copy()
                new_numbers_list.pop(j)
                new_numbers_list.pop(i)
                new_numbers_list.append(combo_result)

                # Call function again with new_numbers_list
                self.calculate_results(new_numbers_list, target)
        # else:
        #     print(numbers)


num_solver = NumbersSolver()
numbers_list = num_solver.initialise(samples,target_num)
print(numbers_list)
num_solver.calculate_results(numbers_list,target_num)
print(num_solver.best)
print(num_solver.counter)