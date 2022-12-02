from models.generator import Generator, GeneratorType

class PropertyMapping():

    @staticmethod
    def empty():
        return PropertyMapping(
            id = "",
            name = "",
            type = "",
            generator = None,
            args = []
        )

    def __init__(
        self, 
        id: str,
        name: str = None, 
        type: GeneratorType = None, 
        generator: Generator = None, 
        # Args to pass into generator during running
        args: list[any] = []):
        self.id = id
        self.name = name
        self.type = type
        self.generator = generator
        self.args = args

    def __str__(self):
        return f"PropertyMapping(id={self.id}, name={self.name}, type={self.type}, generator={self.generator}, args={self.args})"
        
    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.to_string(),
            "generator": self.generator.to_dict(),
            "args": self.args
        }

    def generate_value(self):
        return self.generator.generate(self.args)

