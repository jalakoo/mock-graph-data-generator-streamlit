import random

# Do not change function name or arguments
def generate(args: list[any]):
    min = args[0]
    max = args[1]
    result = random.randint(min, max)
    return result