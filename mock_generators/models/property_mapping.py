from models.generator import Generator, GeneratorType

class PropertyMapping():

    @staticmethod
    def empty():
        return PropertyMapping(
            id = "",
            name = "",
            type = "",
            generator = None,
            generator_args = {}
        )

    def __init__(
        self, 
        id: str,
        name: str = None, 
        type: GeneratorType = None, 
        generator: Generator = None, 
        generator_args: list[any] = []):
        self.id = id
        self.name = name
        self.type = type
        self.generator = generator
        self.generator_args = generator_args

    def __str__(self):
        return f"PropertyMapping(id={self.id}, name={self.name}, type={self.type}, generator={self.generator}, generator_args={self.generator_args})"
        
    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.to_string(),
            "generator": self.generator.to_dict(),
            "generator_args": self.generator_args
        }

