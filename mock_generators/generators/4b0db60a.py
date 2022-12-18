import random
import logging
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:
    # TODO: This doesn't support actual args, just a list of values
    to_node_values = args
    result = random.choice(to_node_values)
    logging.info(f'4b0db60a: result: {result}, values_remaining: {len(to_node_values)}')
    return (result, to_node_values)