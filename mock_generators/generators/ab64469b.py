from datetime import date, timedelta
import random
import logging

# Do not change function name or arguments
def generate(args: list[any]):
    # oldest ISO datetime
    min = args[0]
    # most recent ISO datetime
    max = args[1]
    between = max - min
    logging.info(f'min: {min}, max: {max}, between: {between}')
    days = between.days
    random.seed(a=None)
    random_days = random.randrange(days)
    result = min + timedelta(days=random_days)
    return result