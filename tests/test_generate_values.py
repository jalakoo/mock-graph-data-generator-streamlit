import pytest
from mock_generators.config import load_generators
from mock_generators.logic.generate_values import literal_generator_from_value, actual_generator_for_raw_property, generator_for_raw_property, keyword_generator_for_raw_property, find_longest_float_precision


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
            assert False, f'Exception: {e}'
 

        try:
            # Empty
            test_string = "{}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            assert False, f'Exception: {e}'


        try:
            # Number
            test_string = "6"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            assert False, f'Exception: {e}'
  

        try:
            # Empty
            test_string = ""
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert generator == None
            assert args == None
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_integer(self):
        try:
            test_string = "{\"int\": [1]}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert args == [1]
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == 1
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_integer_list_single(self):
        try:
            test_string = "{\"int_from_list\":[\"1\"]}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert args == ["1"]
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == 1
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_integer_list_multi(self):
        try:
            test_string = "{\"int_from_list\": [\"1,2,3\"]}"
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            assert args == ["1,2,3"]
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1,2,3]
        except Exception as e:
            assert False, f'Exception: {e}'

class TestLiteralSupport:
    def test_find_longest_float_percision(self):
        try:
            test_floats = [1.01, 2.002, 3.004]
            precision = find_longest_float_precision(test_floats)
            assert precision == 3
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            test_floats = [1, -2]
            precision = find_longest_float_precision(test_floats)
            assert precision == 0
        except Exception as e:
            assert False, f'Exception: {e}'

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
             assert False, f'Exception: {e}'


    def test_float(self):
        try:
            test_string = "1.0"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value == 1.0
        except Exception as e:
            assert False, f'Exception: {e}'

    def test_negative_float(self):
        try:
            test_string = "-1.0"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value == -1.0
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_int_range(self):
        try:
            test_string = "1-3"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1,2,3]
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_float_range(self):
        try:
            test_string = "1.0-2"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 2.0
            assert value >= 1.0
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "1-2.0"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 2.0
            assert value >= 1.0
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "1.0-2.0"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 2.0
            assert value >= 1.0
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "1--2.02"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 1.00
            assert value >= -2.01
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "1.01--2.02"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 1.01
            assert value >= -2.01
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            test_string = "-10.0003-20"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 20.0000
            assert value >= -10.0003
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "-10.01-20.02"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= 20.02
            assert value >= -10.01
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "-73--74.004"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= -73.000
            assert value >= -74.004
        except Exception as e:
            assert False, f'Exception: {e}'
        try:
            test_string = "-73.979--74.004"
            generator, args = literal_generator_from_value(test_string, test_generators)
            value = generator.generate(args)
            assert value <= -73.979
            assert value >= -74.004
        except Exception as e:
            assert False, f'Exception: {e}'
    def test_int_list(self):
        try:
            test_string = "[1,2,3]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1,2,3]
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_float_list(self):
        try:
            test_string = "[1.0, 2, 3.0]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in [1.0, 2.0, 3.0], f'generator: {generator}, args: {args}, value: {value}'
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_string(self):
        try:
            test_string = "A string value"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == "A string value"
        except Exception as e:
            assert False, f'Exception: {e}'


    def test_string_from_list(self):
        try:
            test_string = "[Chicken, Peas, Carrots]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = literal_generator_from_value(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in ["Chicken", "Peas", "Carrots"]
        except Exception as e:
            assert False, f'Exception: {e}'

        
class TestGeneratorForProperties:
    def test_failed_generator_for_raw_property(self):
        # Will default to a string literal
        try:
            generator, args = generator_for_raw_property("{\'test_doesnt_exist\':[1]}", test_generators)
            value = generator.generate(args)
            assert value == "{\'test_doesnt_exist\':[1]}"
        except Exception as e:
            assert False, f'Exception: {e}'

    def test_string_routing(self):
        try:
            test_string = "literal string"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = generator_for_raw_property(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value == "literal string"
        except Exception as e:
            assert False, f'Exception: {e}'

    
        try:
            # List of strings
            test_string = "[Chicken, Peas, Carrots]"
            # This should be equivalent to the integer generator with arg of [1]
            generator, args = generator_for_raw_property(test_string, test_generators)
            # Test generator returned creates acceptable value
            value = generator.generate(args)
            assert value in ["Chicken", "Peas", "Carrots"]
        except Exception as e:
            assert False, f'Exception: {e}'



class TestKeywordGeneratorForProperties:
    def test_no_keyword_found(self):
        try:
            generator, args = keyword_generator_for_raw_property("NOT A KEYWORD", test_generators)
            assert generator is None
            assert args is None
        except Exception as e:
            assert False, f'Exception: {e}'

    def test_bool_keywords(self):
        try:
            generator, args = keyword_generator_for_raw_property("bool", test_generators)
            value = generator.generate(args)
            assert value in [True, False]
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            generator, args = keyword_generator_for_raw_property("boolean", test_generators)
            value = generator.generate(args)
            assert value in [True, False]
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            generator, args = keyword_generator_for_raw_property("Boolean", test_generators)
            value = generator.generate(args)
            assert value in [True, False]
        except Exception as e:
            assert False, f'Exception: {e}'

    def test_int_keywords(self):
        try:
            generator, args = keyword_generator_for_raw_property("int", test_generators)
            value = generator.generate(args)
            assert value <= 100
            assert value >= 1
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            generator, args = keyword_generator_for_raw_property("integer", test_generators)
            value = generator.generate(args)
            assert value <= 100
            assert value >= 1
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            generator, args = keyword_generator_for_raw_property("Integer", test_generators)
            value = generator.generate(args)
            assert value <= 100
            assert value >= 1
        except Exception as e:
            assert False, f'Exception: {e}'

    def test_float_keywords(self):
        try:
            generator, args = keyword_generator_for_raw_property("float", test_generators)
            value = generator.generate(args)
            assert value <= 100.0
            assert value >= 1.0
        except Exception as e:
            assert False, f'Exception: {e}'

        try:
            generator, args = keyword_generator_for_raw_property("Float", test_generators)
            value = generator.generate(args)
            assert value <= 100.0
            assert value >= 1.0
        except Exception as e:
            assert False, f'Exception: {e}'

    def test_date_keywords(self):
        from datetime import datetime

        try:
            generator, args = keyword_generator_for_raw_property("date", test_generators)
            value = generator.generate(args)
            lower_bound = datetime.fromisoformat('1970-01-01T00:00:00')
            upper_bound = datetime.fromisoformat('2022-11-24T00:00:00')
            check_date = datetime.fromisoformat(value)
            assert lower_bound <= check_date <= upper_bound
        except Exception as e:
            assert False, f'Exception: {e}'


        try:
            generator, args = keyword_generator_for_raw_property("Datetime", test_generators)
            value = generator.generate(args)
            lower_bound = datetime.fromisoformat('1970-01-01T00:00:00')
            upper_bound = datetime.fromisoformat('2022-11-24T00:00:00')
            check_date = datetime.fromisoformat(value)
            print(f'check_date: {check_date}')
            assert lower_bound <= check_date <= upper_bound
        except Exception as e:
            assert False, f'Exception: {e}'
