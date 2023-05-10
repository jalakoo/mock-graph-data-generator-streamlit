import random
import logging

# Do not change function name or arguments
def generate(args: list[any]):
    try:
        # List should come in wrapped as a string: ie ["1,2,3"]
        options = args[0]
        if options is None or options == "":
            # No args given
            return 0
        
        # Strip white spaces
        # options = options.join(options.split())
        options = options.replace(' ', '')
        options = options.split(',')
        result = int(random.choice(options))
        return result
    except Exception as e:
        logging.error(f'Exception: {e}')
        return None