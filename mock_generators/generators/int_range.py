import random

# Do not change function name or arguments
def generate(args: list[any]):
    min = args[0]
    max = args[1]
    if min == max:
        return min
    return random.randint(min, max)