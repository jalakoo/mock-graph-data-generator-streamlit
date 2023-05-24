from faker import Faker
fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    is_true = args[0]
    result = fake.boolean(chance_of_getting_true=is_true)
    return result