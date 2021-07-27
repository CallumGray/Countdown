from typing import List
from typing import Tuple
from typing import Set
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
# Algorithm for solving numbers
#
#

class NumbersSolver:

    def __init__(self):
        # List as it needs to be indexable
        self.bests: List[int] = [0]
        # Set to avoid duplicates
        self.best_exprs: Set[str] = {''}
        self.counter: int = 0

    # See if the number is the closest to the target
    def compare_to_best(self, n: Tuple[int, str], target: int):
        num = n[0]
        expr = n[1]

        # As good as existing best
        if abs(target - num) == abs(target - self.bests[0]):

            self.best_exprs.append(expr)

            if not num in self.bests:
                self.bests.append(num)

        # Better than existing best
        elif abs(target - num) < abs(target - self.bests[0]):
            self.bests = [num]
            self.best_exprs = [expr]

    # Custom function similar to itertools.combinations(xs,2), but also
    # yields the indexes of each combination from within the original list
    def custom_combo(self, xs: List):
        for i, xi in enumerate(xs):
            for j, xj in enumerate(xs):
                if i < j:
                    yield (xi, xj, i, j)

    # Get list of all values that can be made from 2 integers
    def operation_results(self, a: Tuple[int, str], b: Tuple[int, str]) -> List[Tuple[int, str]]:

        # Order matters for subtraction and division so need to find the biggest and smallest
        (big_num,big_expr, small_num,small_expr) = (a[0],a[1],b[0],b[1]) if a[0] > b[0] else (b[0],b[1],a[0],a[1])

        add: Tuple[int, str] = (big_num + small_num, '(' + big_expr + '+' + small_expr + ')')
        mult: Tuple[int, str] = (big_num * small_num, '(' + big_expr + '*' + small_expr + ')')
        sub: Tuple[int, str] = (big_num - small_num, '(' + big_expr + '-' + small_expr + ')')

        self.counter += 3

        # Division is invalid if divisor is 0 or it doesn't result in an integer
        if small_num == 0 or big_num % small_num != 0:
            return [add, sub, mult]

        div: Tuple[int, str] = (big_num // small_num, '(' + big_expr + '/' + small_expr + ')')
        self.counter += 1

        return [add, sub, mult, div]

    # All operation_results between 2 lists
    def list_operations(self, alist: List[Tuple[int, str]], blist: List[Tuple[int, str]]) -> List[Tuple[int, str]]:

        final_list: List[Tuple[int, str]] = []

        for a in alist:
            for b in blist:
                final_list += self.operation_results(a, b)

        return final_list

    # Set best to default and set the numbers to the form [[x],[y],[z] ... ]
    def initialise(self, numbers: List[int], target: int) -> List[List[Tuple[int, str]]]:

        # set best to 0
        self.best = [0]
        self.best_expr = {''}

        # Using all of the numbers on their own
        for n in numbers:
            self.compare_to_best((n, str(n)), target)

        # return numbers as a list of lists [[x],[y],[z] ... ]
        return [[(n, str(n))] for n in numbers]

    # Numbers must be supplied in the form [[x],[y],[z] ... ] to simplify the algorithm.
    # Since list_operations returns a list, the values in numbers must be lists too.
    def calculate_results(self, numbers: List[List[Tuple[int, str]]], target: int):

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


def print_solution(solver: NumbersSolver, numbers: List[int], target_num: int):

    print("TARGET: ", target_num)

    numbers_list = solver.initialise(numbers, target_num)
    print([n[0][0] for n in numbers_list], "\n")
    solver.calculate_results(numbers_list, target_num)

    print('BEST:')
    for best in solver.bests:
        print(best)

    print()

    print('BEST EXPRESSIONS:\n')
    for best_expr in solver.best_exprs:
        print(best_expr,"\n")

    # print('Calculations:',num_solver.counter)


while True:
    mode: str = ''

    while mode != 'R' and mode != 'C' and mode != 'X':
        mode = input("Random [R], Chosen [C], Exit [X]\n").upper()

    if mode == 'R':

        n_bigs: int = -1

        while not 0 <= n_bigs <= 6:

            try:
                n_bigs = int(input('How many big numbers? (0 to 6) \n'))
                if not 0 <= n_bigs <= 6:
                    print("Enter an integer between 0 and 6\n")
            except ValueError:
                print("Enter an integer between 0 and 6\n")

        n_smalls: int = 6 - n_bigs
        print(n_bigs, ' big numbers, ', n_smalls, ' small numbers\n')
        samples: List[int] = sample_numbers(n_bigs, n_smalls)
        print_solution(num_solver, samples, target())


    # Choose numbers
    elif mode == 'C':

        ints: List[int] = []

        # Ask user to choose 9 letters
        while len(ints) < 6:
            try:
                int_prompt = int(input("Number " + str(len(ints) + 1) + ":\n"))
                ints.append(int_prompt)

            except ValueError:
                print("Invalid")

        target_prompt = None

        while not target_prompt:

            try:
                target_prompt = int(input("Target:\n"))
            except ValueError:
                print("Invalid")

        print_solution(num_solver,ints,target_prompt)

    # Exit
    elif mode == 'X':
        break
