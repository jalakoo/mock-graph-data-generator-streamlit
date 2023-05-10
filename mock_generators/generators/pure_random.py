import random
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    targets = args[:]
    result = random.choice(targets)
    return (result, targets)