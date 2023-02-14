from faker import Faker
fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    result = None
    if len(args) != 0:
        domain = args[0]
        if domain != "" and domain is not None:
            result = fake.email(domain=domain)
    if result is None:
        result = fake.email()

    return result