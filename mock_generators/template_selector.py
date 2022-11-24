# from template_generators.bool_generator import BoolGenerator
# from template_generators.datetime_generator import DatetimeGenerator
# from template_generators.float_generator import FloatGenerator
# from template_generators.int_generator import IntGenerator
# from template_generators.string_generator import StringGenerator

def pathFrom(type: str):
    type = type.lower()
    if type == "string":
        return "mock_generators/template_generators/string_generator.py"
    elif type == "int":
        return "mock_generators/template_generators/int_generator.py"
    elif type == "float":
        return "mock_generators/template_generators/float_generator.py"
    elif type == "datetime":
        return "mock_generators/template_generators/datetime_generator.py"
    elif type == "bool":
        return "mock_generators/template_generators/bool_generator.py"
    else:
        raise TypeError("Type not supported")

def templateFromType(type: str):
    path = pathFrom(type)
    with open(path, "r") as file:
        return file.read()

def generic_template():
    with open("mock_generators/template_generators/generic_generator.py", "r") as file:
        return file.read()