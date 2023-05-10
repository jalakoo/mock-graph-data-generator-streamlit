import random

# Do not change function name or arguments
def generate(args: list[any]):
    width = 400
    height = 200
    if len(args) > 1:
        try:
            height = int(args[1])
        except:
            pass
    if len(args) > 0:
        try:
            width = int(args[0])
        except:
            pass
    
    pid = random.randint(1, 237)
    url = f'https://picsum.photos/id/{pid}/{width}/{height}'
    return url