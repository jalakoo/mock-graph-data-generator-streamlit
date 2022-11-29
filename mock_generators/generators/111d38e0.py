import random
import logging

# Do not change function name or arguments
def generate(args: list[any]):
    options = args[0]
    if options is None or options == "":
        return []
    options = options.replace(' ', '')
    options = options.split(',')
    result = float(random.choice(options))
    return result