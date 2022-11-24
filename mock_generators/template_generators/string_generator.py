from base_generators.string_generator import StringGenerator
# <add_custom_imports_here>

class Generator(StringGenerator):
    def __init__(self, name: str, description: str, generator: callable, **kwargs):
        super().__init__(name, description, generator, **kwargs)

    def generate(self, *args):
        # <replace_with_custom_code_here>
        pass