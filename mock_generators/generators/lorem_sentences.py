from lorem_text import lorem
import random

def generate(args: list[any]):
    min = args[0]
    max = args[1]
    num = random.randint(min, max)
    result = lorem.sentence()
    for _ in range(num):
       result += " " + lorem.sentence()
    return result