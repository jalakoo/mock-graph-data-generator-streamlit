from base_generators.datetime_generator import DatetimeGenerator
# <add_custom_imports_here>


class Generator(DatetimeGenerator):
    def __init__(self, name: str, description: str, generator: callable, **kwargs):
        super().__init__(name, description, generator, **kwargs)

    def generate(self, *args):
        # <custom_code_here>
        pass