import random
import logging
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:
    # logging.info(f'4b0db60a: args: {args}')
    to_node_values = args
    result = random.choice(to_node_values)
    # logging.info(f'4b0db60a: result: {result}')
    return (result, to_node_values)