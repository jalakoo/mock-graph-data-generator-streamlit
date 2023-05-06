import os
import pytest
from mock_generators.config import load_generators
from mock_generators.logic.generate_values import actual_generator_for_raw_property
from datetime import datetime
test_generators = load_generators("mock_generators/named_generators.json")

class TestDateGenerator:
    def test_date_generator(self):
        try:
            test_string = '{"date": ["1970-01-01", "2022-11-24"]}'
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            value = generator.generate(args)

            lower_bound = datetime.fromisoformat('1970-01-01T00:00:00')
            upper_bound = datetime.fromisoformat('2022-11-24T00:00:00')

            # define a datetime object to check
            check_date = datetime.fromisoformat(value)

            # check if the check_date is within the bounds
            assert lower_bound <= check_date <= upper_bound
        except Exception as e:
            print(f'Exception: {e}')
            assert False

        try:
            test_string = '{"date": ["1970-01-01", "1970-01-01"]}'
            generator, args = actual_generator_for_raw_property(test_string, test_generators)
            value = generator.generate(args)

            lower_bound = datetime.fromisoformat('1970-01-01T00:00:00')
            upper_bound = datetime.fromisoformat('1970-01-01T00:00:00')

            # define a datetime object to check
            check_date = datetime.fromisoformat(value)

            # check if the check_date is within the bounds
            assert lower_bound <= check_date <= upper_bound
        except Exception as e:
            print(f'Exception: {e}')
            assert False