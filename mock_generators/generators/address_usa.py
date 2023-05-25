from random_address import real_random_address
import random

def generate(args: list[any]):
    # Generate a dictionary with valid random address information
    # states = [
    #     "AL", "AR", "CA", "CO", "CT", "DC", "FL", "GA", "HI", "KY", "MA" "MD", "TN", "TX", "OK", "VT"
    # ]
    # state_code = random.choice(states)
    # return real_random_address_by_state(state_code)
    return real_random_address()

def generate(args: list[any]):
    # Generate a dictionary with valid random address information
    states = [
        "AL", "AR", "CA", "CO", "CT", "DC", "FL", "GA", "HI", "KY", "MA" "MD", "TN", "TX", "OK", "VT"
    ]
    state_code = random.choice(states)
    return real_random_address_by_state(state_code)