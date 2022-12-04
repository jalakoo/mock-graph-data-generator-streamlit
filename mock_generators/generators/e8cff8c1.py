import random

# Do not change function name or arguments
def generate(args: list[any]):
    min = args[0]
    max = args[1]
    decimal_places = args[2]
    result = round(random.uniform(min, max), decimal_places)
    return result