from models.generator import Generator, GeneratorType
from list_utils import clean_list
import logging

class PropertyMapping():

    @staticmethod
    def empty():
        return PropertyMapping(
            pid = None,
            name = None,
            # type = None,
            generator = None,
            args = None
        )

    def __init__(
        self, 
        pid: str,
        name: str = None, 
        # type: GeneratorType = None, 
        generator: Generator = None, 
        # Args to pass into generator during running
        args: list[any] = []):
        self.pid = pid
        self.name = name
        # self.type = type
        self.generator = generator
        self.args = args

    def __str__(self):
        name = self.name if self.name is not None else "<unnamed>"
        generator = self.generator if self.generator is not None else "<no_generator_assigned>"
        return f"PropertyMapping(pid={self.pid}, name={name}, generator={generator}, args={self.args}"
        
    def __repr__(self):
        return self.__str__()

    def __equ__(self, other):
        return self.pid == other.pid

    def to_dict(self):
        return {
            "pid": self.pid,
            "name": self.name,
            # "type": self.type.to_string() if self.type is not None else None,
            "generator": self.generator.to_dict() if self.generator is not None else None,
            "args": clean_list(self.args)
        }

    def ready_to_generate(self):
        if self.name is None:
            return False
        # if self.type is None:
        #     return False
        if self.generator is None:
            return False
        return True

    def generate_value(self):
        if self.generator == None:
            logging.error(f'property_mapping.py: generate_value: Generator is not set for property {self.name}')
        if isinstance(self.args, list) == False:
            logging.error(f'property_mapping.py: generate_value: Args for generator is not a list for property {self.name}')
        result = self.generator.generate(self.args)
        return result

