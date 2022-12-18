from random import shuffle
import logging

# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    # TODO: This doesn't support actual args, just a list of values
    node_values = args
    shuffle(node_values)
    choice = node_values.pop(0)
    # logging.info(f'73853311: choice: {choice}, values remaining: {len(node_values)}')
    return (choice, node_values)