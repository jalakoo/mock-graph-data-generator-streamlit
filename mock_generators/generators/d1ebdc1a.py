from faker import Faker
fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    result = fake.catch_phrase()
    return result