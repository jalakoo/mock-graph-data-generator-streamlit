from base_generators.bool_generator import BoolGenerator
# <add_custom_imports_here>


class Generator(BoolGenerator):
    def __init__(self, name: str, description: str, generator: callable, **kwargs):
        super().__init__(name, description, generator, **kwargs)

    def generate(self, *args):
        # <custom_code_here>
        pass