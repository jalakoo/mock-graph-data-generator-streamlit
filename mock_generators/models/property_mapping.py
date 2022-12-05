from models.generator import Generator, GeneratorType
import logging

class PropertyMapping():

    @staticmethod
    def empty():
        return PropertyMapping(
            id = None,
            name = None,
            type = None,
            generator = None,
            args = None
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
        return f"PropertyMapping(id={self.id}, name={self.name}, type={self.type}, generator={self.generator.name}, generator_id={self.generator.id}, args={self.args})"
        
    def __repr__(self):
        return self.__str__()

    def __equ__(self, other):
        return self.id == other.id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.to_string(),
            "generator": self.generator.to_dict(),
            "args": self.args
        }

    def generate_value(self):
        if self.generator == None:
            logging.error(f'Generator is not set for property {self.name}')
        result = self.generator.generate(self.args)
        return result

