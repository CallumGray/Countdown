from typing import List
from typing import Tuple
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
        self.best_expr: str = ''
        self.counter: int = 0

    # See if the number is the closest to the target
    def compare_to_best(self, n: Tuple[int,str], target: int):
        num = n[0]
        expr = n[1]

        if abs(target - num) < abs(target - self.best):
            self.best = num
            self.best_expr = expr

    # Custom function similar to itertools.combinations(xs,2), but also
    # yields the indexes of each combination from within the original list
    def custom_combo(self, xs: List):
        for i, xi in enumerate(xs):
            for j, xj in enumerate(xs):
                if i < j:
                    yield (xi, xj, i, j)

    # Get list of all values that can be made from 2 integers
    def operation_results(self, a: Tuple[int,str], b: Tuple[int,str]) -> List[Tuple[int,str]]:

        # Numeric value
        a_num = a[0]
        b_num = b[0]

        # Mathematical expression leading up to numeric value
        a_expr = a[1]
        b_expr = b[1]

        # Order doesn't matter for addition and multiplication
        add: Tuple[int,str] = (a_num + b_num,'('+a_expr+'+'+b_expr+')')
        mult: Tuple[int,str] = (a_num * b_num,'('+a_expr+'*'+b_expr+')')

        # Order matters for subtraction and division
        (bigger, smaller) = ((a_num,a_expr), (b_num,b_expr)) if a_num > b_num else ((b_num,b_expr), (a_num,a_expr))

        sub: Tuple[int,str] = (bigger[0] - smaller[0],'('+bigger[1]+'-'+smaller[1]+')')

        self.counter += 3

        # Division is invalid if divisor is 0 or it doesn't result in an integer
        if smaller[0] == 0 or bigger[0] % smaller[0] != 0:
            return [add, sub, mult]

        div: Tuple[int,str] = (bigger[0] // smaller[0],'('+bigger[1]+'/'+smaller[1]+')')
        self.counter += 1

        return [add, sub, mult, div]

    # All operation_results between 2 lists
    def list_operations(self, alist: List[Tuple[int,str]], blist: List[Tuple[int,str]]) -> List[Tuple[int,str]]:

        final_list: List[Tuple[int,str]] = []

        for a in alist:
            for b in blist:
                final_list += self.operation_results(a, b)

        return final_list

    # Set best to default and set the numbers to the form [[x],[y],[z] ... ]
    def initialise(self, numbers: List[int], target: int) -> List[List[Tuple[int,str]]]:

        # set best to 0
        self.best = 0
        self.best_expr = ''

        # Using all of the numbers on their own
        for n in numbers:
            self.compare_to_best((n,str(n)), target)

        # return numbers as a list of lists [[x],[y],[z] ... ]
        return [[(n,str(n))] for n in numbers]

    # Numbers must be supplied in the form [[x],[y],[z] ... ] to simplify the algorithm.
    # Since list_operations returns a list, the values in numbers must be lists too.
    def calculate_results(self, numbers: List[List[Tuple[int,str]]], target: int):

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


num_solver = NumbersSolver()
numbers_list = num_solver.initialise(samples,target_num)
print([n[0][0] for n in numbers_list])
num_solver.calculate_results(numbers_list,target_num)
print('Best:',num_solver.best)
print(num_solver.best_expr)
print('Calculations:',num_solver.counter)