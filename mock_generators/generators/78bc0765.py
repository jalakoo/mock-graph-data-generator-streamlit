from faker import Faker
fake = Faker()

def generate(args: list[any]):
    limit = args[0]
    result = fake.uuid4()[:limit]
    return result