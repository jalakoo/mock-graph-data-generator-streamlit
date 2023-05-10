from faker import Faker
fake = Faker()

def generate(args: list[any]):
    return fake.street_address()