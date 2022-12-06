import random

# Do not change function name or arguments
def generate(args: list[any]):
    options = args[0]
    if options is None or options == "":
        return 0
    options = options.replace(' ', '')
    options = options.split(",")
    result = int(random.choice(options))
    return result