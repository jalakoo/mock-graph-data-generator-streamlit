import random

# Do not change function name or arguments
def generate(args: list[any]):
    random.seed()
    options = str(args[0])
    options = options.replace(' ', '')
    options = options.split(",")
    result = random.choice(options)
    return result