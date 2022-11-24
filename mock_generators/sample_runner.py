

def run(generator_spec : dict, generator : any, *args):
    """
    Runs a generator with the given arguments.
    :param generator_spec: The generator specification.
    :param generator: The generator.
    :param args: The arguments to pass to the generator.
    :return: The generated value.
    """
    # <custom_code_here>
    return generator.generate(*args)