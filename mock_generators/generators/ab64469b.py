from datetime import timedelta
import random

# Do not change function name or arguments
def generate(args: list[any]):
    # oldest ISO datetime
    min = args[0]
    # most recent ISO datetime
    max = args[1]
    between = max - min
    days = between.days
    random.seed(a=None)
    random_days = random.randrange(days)
    result = min + timedelta(days=random_days)
    return result