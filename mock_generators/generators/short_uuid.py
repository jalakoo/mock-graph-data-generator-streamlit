from faker import Faker
fake = Faker()

def generate(args: list[any]=[]):
    if len(args) == 0:
        result = fake.uuid4()
    else:
        limit = args[0]
        result = fake.uuid4()[:limit]
    return result