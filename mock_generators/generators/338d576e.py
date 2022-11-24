import random
from lorem_text import lorem

def generate(args: list[any]):
    min = args[0]
    max = args[1]
    num = random.randint(min, max)
    return lorem.paragraphs(num)