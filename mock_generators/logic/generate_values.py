
from models.generator import Generator, GeneratorType
import logging
import json

# ORIGINAL GENERATOR ASSIGNMENT
def actual_generator_for_raw_property(
    property_value: str, 
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """Returns a generator and args for a property. Returns None if not found."""
    # Sample property_values: 
    #   "{\"company_name\":[]}"
    #   {"int_from_list": ["1,2,3"]}
    try:
        obj = json.loads(property_value)
        # Should only ever be one
        for key, value in obj.items():
            generator_id = key
            generator = generators.get(generator_id, None)
            if generator is None:
                logging.error(f'Generator_id {generator_id} not found in generators. Skipping generator assignment for property_value: {property_value}')
                return (None, None)
            args = value
            return (generator, args)
    except Exception as e:
        logging.debug(f'Could not parse JSON string: {property_value}. Returning None from generator assignment for property_value: {property_value}. Error: {e}')

    return (None, None)

# KEYWORD GENERATOR ASSIGNMENT
def keyword_generator_for_raw_property(
    value: str,
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """Returns a generator and args for a property value using a generic keyword. Returns None if not found."""

    result = None
    if value.lower() == "string":
            result = {
                "lorem_words": [1,3]
            }
    elif value.lower() == "int" or value.lower() == "integer":
            result = {
                "int_range": [1,100]
            }
    elif value.lower() == "float":
            result = {
                "float_range": [1.0,100.0, 2]
            }
    elif value.lower() == "bool" or value.lower() == "boolean":
            result = {
                "bool": [50]
            }
    elif value.lower() == "date" or value.lower() == "datetime":
            result = {
                "date": ["1970-01-01", "2022-11-24"]
            }

    # Default
    if result is None:
        return (None, None)
    
    # Generator was assigned
    g_config = json.dumps(result)
    return actual_generator_for_raw_property(g_config, generators)


# LITERAL GENERATOR ASSIGNMENT SUPPORT
def all_ints(values: list[str]) -> bool:
    for value in values:
        if not is_int(value):
            return False
    return True

def some_floats(values: list[str]) -> bool:
    for value in values:
        if is_float(value):
            return True
    return False

def all_floats(values: list[str]) -> bool:
    for value in values:
        if not is_float(value):
            return False
    return True

def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def is_float(value: str) -> bool:
    try:
        f = float(value)
        return True
    except ValueError:
        return False
    
def literal_generator_from_value(
        value: str,
        generators: list[Generator]
    )-> tuple[Generator, list[any]]:
    """
        Attempts to find an actual generator based on more concise literal values from arrows.app JSON

        Support for:
            - ints
            - floats
            - ranges of ints
            - ranges of floats
            - lists of ints
            - lists of floats
            - string literals
            - list of strings

        TODO:
            - bools
            - lists of bools
            - date
            - lists of dates
            - datetime (ISO 8601)
            - list of datetimes
    """
    # Sample expected values: 
    #   "1"
    #   "1-10"
    #   "[3, 5, 10]"
    #   "[Yes, No]"
    #   "[True, False, False]"

    # Original specificaion took stringified JSON objects to notate generator and args to use. We're going to convert matching literal values to appropriate generators
    
    # Default is to use the literal generator
    result = {
        "string": [value]
    }

    # Check if value is an int or float
    if is_int(value):
        integer = int(value)
        result = {
            "int": [integer]
        }

    if is_float(value):
        f = float(value)
        result = {
            "float": [f]
        }

    # NOTE: Not currently handling complex literals
     
    # Check if value is a range of ints or floats
    r = value.split("-")
    if len(r) == 2:
        # Single dash in string, possibly a literal range
        values = [r[0], r[1]]
        if all_ints(values):
            result = {
                "int_range": [int(r[0]), int(r[1])]
            }
        elif some_floats(values):
            # Float range function expects 3 args - this one seems more sensible than other functions
            result = {
                "float_range": [float(r[0]), float(r[1]), 2]
            }
 

    # Check for literal list of ints, floats, or strings
    if value.startswith('[') and value.endswith(']'):
        values = value[1:-1].split(',')
        # Generators take a strange format where the args are always a string - including # lists of other data, like ints, floats. ie ["1,2,3"] is an expected arg type
        # because certain generators could take multiple args from different text fields
        # These literals, however, all only take a single generic arg

        # YES - this is terrible
        
        if all_ints(values):
            ints_as_string = ",".join([f'{int(v)}' for v in values])
            result = {
                "int_from_list": [f"{ints_as_string}"]
            }
        elif some_floats(values):
            floats_as_string = ",".join([f'{float(v)}' for v in values])
            result = {
                "float_from_list": [f"{floats_as_string}"]
            }
        else:
            result = {
                "string_from_list": values
            }

    # Package and return from legacy process
    actual_string = json.dumps(result)
    return actual_generator_for_raw_property(actual_string, generators)

def assignment_generator_for(
    config: str,
    generators: dict[str, Generator]
) -> tuple[Generator, list[any]]:
    
    gen, args =  actual_generator_for_raw_property(config, generators)
    if gen.type != GeneratorType.ASSIGNMENT:
        logging.error(f'Generator {gen.name} is not an assignment generator.')
        return (None, None)
    return gen, args

def generator_for_raw_property(
    property_value: str, 
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """
        Returns a generator and args for specially formatted property values from the arrows.app JSON file. Attempts to determine if literal or original generator
        specification was use.

        Return None if no generator found.
    """

    # Original Sample expected string: "{\"company_name\":[]}"
    # New literal examples: 
    #     "{\"company_name\":\"Acme\"}"
    #     "{\"company_name\":[\"Acme\"]}"
    #     "{\"company_name\":\"string\"}"

    # Also fupport following options: "string", "bool", "boolean", "float", "integer", "number", "date", "datetime"

    generator, args = None, None

    # Check for Legacy Properties assignments
    # Also returns None, None if no matching generator found
    if generator is None:
        generator, args = keyword_generator_for_raw_property(property_value, generators)

    if generator is None:
        generator, args = actual_generator_for_raw_property(property_value, generators)

    # Check for new literal assignments
    # Defaults to string literal
    if generator is None: 
        generator, args = literal_generator_from_value(property_value, generators)

    return (generator, args)