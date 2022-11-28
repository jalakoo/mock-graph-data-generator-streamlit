from enum import Enum
import logging

class GeneratorType(Enum):
    BOOL = 1,
    INT = 2,
    FLOAT = 3,
    STRING = 4,
    DATETIME = 5

    @staticmethod
    def type_from_string(aType: str):
        type = aType.lower()
        if type == "string":
            return GeneratorType.STRING
        elif type == "int":
            return GeneratorType.INT
        elif type == "float":
            return GeneratorType.FLOAT
        elif type == "datetime":
            return GeneratorType.DATETIME
        elif type == "bool":
            return GeneratorType.BOOL
        else:
            raise TypeError("Type not supported")
    
    def to_string(self):
        if self == GeneratorType.STRING:
            return "String"
        elif self == GeneratorType.INT:
            return "Int"
        elif self == GeneratorType.FLOAT:
            return "Float"
        elif self == GeneratorType.DATETIME:
            return "Datetime"
        elif self == GeneratorType.BOOL:
            return "Bool"
        else:
            raise TypeError("Type not supported")


class GeneratorArg():

    @staticmethod
    def from_dict(dict: dict):
        if "type" not in dict.keys():
            raise KeyError("Arg dict missing type key")
        if "label" not in dict.keys():
            raise KeyError("Arg dict missing label key")
        if "default" not in dict.keys():
            default = None
        else: 
            default = dict["default"]

        return GeneratorArg(
            type = GeneratorType.type_from_string(dict["type"]),
            label = dict["label"],
            default= default
        )

    def __init__(
        self, 
        type: GeneratorType, 
        label: str,
        default: any = None
    ):
        self.type = type
        self.label = label
        self.default = default

    def to_dict(self):
        return {
            "type": self.type.to_string(),
            "label": self.label,
            "default": self.default
        }

    @staticmethod
    def list_from(list: list[dict]):
        return [GeneratorArg.from_dict(item) for item in list]


def generators_from_json(json : dict) -> dict:
    result = {}
    for key in json.keys():
        generator = Generator.from_dict(key, json[key])
        result[key] = generator
    return result

class Generator():

    @staticmethod
    def from_dict(
        id: str,
        generator_dict: dict
    ):
        if 'name' not in generator_dict.keys():
            raise Exception("Generator must have a name")
        if 'type' not in generator_dict.keys():
            raise Exception("Generator must have a type")
        if 'description' not in generator_dict.keys():
            raise Exception("Generator must have a description")
        if 'code_url' not in generator_dict.keys():
            raise Exception("Generator must have code")
        if 'args' not in generator_dict.keys():
            args = []
        else :
            args = GeneratorArg.list_from(generator_dict['args'])
        # if "packages" not in generator_dict.keys():
        #     packages = []
        # else:
        #     packages = generator_packages_from(generator_dict["packages"])
        
        return Generator(
            id = id,
            type = GeneratorType.type_from_string(generator_dict['type']),
            name = generator_dict['name'],
            description = generator_dict['description'],
            # packages = packages,
            code_url = generator_dict['code_url'],
            args = args
        )

    def __init__(
        self, 
        id: str,
        type : GeneratorType, 
        name: str, 
        description: str, 
        code_url: str,
        args: list[GeneratorArg],
        # packages: list[GeneratorPackage]
        ):
        self.id = id
        self.name = name
        self.description = description
        self.code_url = code_url
        self.args = args
        self.type = type
    
    def import_url(self):
        trimmed = self.code_url.split("/", 1)[1]
        return trimmed.replace("/", ".").replace(".py", "")

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "code_url": self.code_url,
            "args": [arg.to_dict() for arg in self.args],
            "type": self.type.to_string()
        }

    def __str__(self):
        return f'Generator: id: {self.id}, name: {self.name}'

    def __repr__(self):
        return self.__str__()

    def run(self, *args):
        module = __import__(self.import_url(), fromlist=['generate'])
        # logging.info(f'arg_inputs: {arg_inputs}')
        return module.generate(args)

def generators_dict_to_json(dict: dict[str, Generator]) -> str:
    return {key: value.to_dict() for key, value in dict.items()}

def generators_list_to_json(list: list[Generator]) -> str:
    return [generator.to_dict() for generator in list]