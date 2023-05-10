from datetime import datetime, timedelta
import random

# Do not change function name or arguments
def generate(args: list[any]):
    # oldest ISO datetime
    min = args[0]
    # most recent ISO datetime
    max = args[1]

    # Convert string args to datetime
    min_date = datetime.fromisoformat(min)
    max_date = datetime.fromisoformat(max)

    delta = max_date - min_date
    result = min_date + timedelta(seconds=random.randint(0, delta.total_seconds()))

    # Data Importer expects a string in ISO format
    return result.isoformat()