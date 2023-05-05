import pytest
from mock_generators.config import load_generators
from mock_generators.logic.generate_values import literal_generator_from_value, actual_generator_for_raw_property, generator_for_raw_property


test_generators = load_generators("mock_generators/named_generators.json")

# TODO: Probably not the most ideal way to test these

class TestActualGenerators:

    def test_non_conforming(self):
        try:
            # String literal
            test_string = "invalid"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            print(f'Exception: {e}')
            assert False    

        try:
            # Empty
            test_string = "{}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            print(f'Exception: {e}')
            assert False   

        try:
            # Number
            test_string = "6"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            print(f'Exception: {e}')
            assert False   

        try:
            # Empty
            test_string = ""
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            print(f'Exception: {e}')
            assert False  

    def test_integer(self):
        try:
            test_string = "{\"int\": [1]}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert args == [1]
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == 1
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_integer_list_single(self):
        try:
            test_string = "{\"int_from_list\":[\"1\"]}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert args == ["1"]
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == 1
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_integer_list_multi(self):
        try:
            test_string = "{\"int_from_list\": [\"1,2,3\"]}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert args == ["1,2,3"]
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1,2,3]
        except Exception as e:
            print(f'Exception: {e}')
            assert False

class TestLiteralGenerators:
    def test_integer(self):
        try:
            test_string = "1"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == 1
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_float(self):
        try:
            test_string = "1.0"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == 1.0
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_int_range(self):
        try:
            test_string = "1-3"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1,2,3]
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_float_range(self):
        try:
            test_string = "1.0-2"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value <= 2.0
            assert value >= 1.0
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_int_list(self):
        try:
            test_string = "[1,2,3]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1,2,3]
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_float_list(self):
        try:
            test_string = "[1.0, 2, 3.0]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1.0, 2.0, 3.0], f'generator: {generator}, args: {args}, value: {value}'
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_string(self):
        try:
            test_string = "A string value"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == "A string value"
        except Exception as e:
            print(f'Exception: {e}')
            assert False

    def test_string_from_list(self):
        try:
            test_string = "[Chicken, Peas, Carrots]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in ["Chicken", "Peas", "Carrots"]
        except Exception as e:
            print(f'Exception: {e}')
            assert False
        
class TestGeneratorForProperties:
    def test_failed_generator_for_raw_property(self):
        try:
            generator, args = generator_for_raw_property("{\'test_doesnt_exist\':[1]}", test_generators)
            assert generator is None
            assert args is None
        except Exception as e:
            print(f'Exception: {e}')

    def test_string_routing(self):
        try:
            test_string = "literal string"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = generator_for_raw_property(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == "literal string"
        except Exception as e:
            print(f'Exception: {e}')
            assert False
    
        try:
            # List of strings
            test_string = "[Chicken, Peas, Carrots]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = generator_for_raw_property(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in ["Chicken", "Peas", "Carrots"]
        except Exception as e:
            print(f'Exception: {e}')
            assert False