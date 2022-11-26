from faker import Faker
fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    domain = args[0]
    if domain is None:
        result = fake.email()
    else:
        result = fake.email(domain=domain)
    return result