from faker import Faker
fake = Faker()

def generate(args: list[any]):
    limit = args[0]
    result = fake.uuid4(raw_output=False)[:limit]
    return result