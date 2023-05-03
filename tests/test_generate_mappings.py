import os
import pytest

from mock_generators.models.generator import Generator, GeneratorType, GeneratorArg
from mock_generators.models.node_mapping import NodeMapping
from mock_generators.generate_mapping import generator_for_raw_property, mapping_from_json, propertymappings_for_raw_properties, node_mappings_from

import json
import logging

int_args_test = GeneratorArg(
        type=GeneratorType.INT,
        label="test_arg",
        default=1,
    )

int_generator_test = Generator(
        id="test_int",
        name="test_int",
        type=GeneratorType.INT,
        description="test",
        args=[int_args_test],
        code_url="mock_generators/generators/ecdff22c.py",
        tags=["int, integer, number"]
    )

float_args_test = [
    GeneratorArg(
        type=GeneratorType.FLOAT,
        label="min",
        default=1.0,
    ),
    GeneratorArg(
        type=GeneratorType.FLOAT,
        label="max",
        default=2.0,
    ),
    ]

float_generator_test = Generator(
        id="test_float",
        name = "test_float",
        type=GeneratorType.FLOAT,
        description="test",
        args=float_args_test,
        code_url="mock_generators/generators/e8cff8c1.py",
        tags=["float", "number"]
    )

test_generators = {
    "test_int" : int_generator_test,
    "test_float" : float_generator_test
}

class TestClass:

    # def test_version(self):
    #     assert __version__ == "0.1.0"

    def test_generator(self):
        generator = Generator(
            id="test",
            name="test",
            type=GeneratorType.INT,
            description="test",
            args=[],
            code_url="",
            tags = ["test"]
        )
        assert generator.id == "test"
        assert generator.name == "test"
        assert generator.type == GeneratorType.INT
        assert generator.description == "test"
        assert generator.args == []
        assert generator.code_url == ""
        # TODO: Why is this not working
        # tag_check = generator.tags("test")
        # assert tag_check > 0

    def test_jsonification(self):
        # Parsing json strings critical to this class
        json_string = "{\"test_int\":[1]}"
        try:
            obj = json.loads(json_string)
            items = obj.items()
            assert items is not None
            assert len(items) == 1
            for key, value in items:
                assert key == "test_int"
                assert value == [1]

            value = obj.get('test_int', None)
            assert value is not None
            assert value == [1]
        except Exception as e:
            print(f'Exception: {e}')
            assert False
        

    def test_generator_for_raw_property(self):
        try:
            test_string = "{\"test_int\":[1]}"
            generator, args = generator_for_raw_property(test_string, test_generators)
        except Exception as e:
            print(f'Exception: {e}')
        # if status_message is not None:
        #     print(f'status: {status_message}')
        assert int_generator_test is not None
        assert int_args_test is not None
        assert generator == int_generator_test
        assert args == [1]
        # Test generator returned creates acceptable value
        value = generator.generate(args)
        assert value == 1

    def test_failed_generator_for_raw_property(self):
        try:
            generator, args = generator_for_raw_property("{\'test_doesnt_exist\':[1]}", test_generators)
        except Exception as e:
            print(f'Exception: {e}')
        assert generator is None
        assert args is None

    def test_propertymappings_for_raw_properties_smoke(self):
        raw_props = {
                "alpha": "{\"test_int\":[1]}",
                "bravo": "{\"test_float\":[1.0, 2.0]}"
            }
        mappings = propertymappings_for_raw_properties(
            raw_properties=raw_props,
            generators= test_generators)
        assert len(mappings) == 2


    # def test_node_mappings_from(self):
    #     nodes = node_mappings_from(
    #         node_dicts=[{
    #             "id": "n1",
    #             "position": {
    #             "x": 284.5,
    #             "y": -204
    #             },
    #             "caption": "Company",
    #             "labels": [],
    #             "properties": {
    #                 "uuid": "{\"test_float\":[8]}",
    #                 "{count}": "{\"test_int\":[1]}",
    #                 "{key}": "uuid"
    #             },
    #             "style": {}
    #         }],
    #         generators= test_generators
    #     )
    #     expectedNodeMapping = NodeMapping(
    #         nid="n1",
    #         position={
    #             "x": 284.5,
    #             "y": -204
    #         },
    #         caption="Company",
    #         labels=[],
    #         properties={
    #             "uuid": "{{\"test_float\":[8]}}",
    #             "{count}": "{{\"test_int\":[1]}}",
    #             "{key}": "uuid"
    #         },
    #         count_generator=int_generator_test,
    #         count_args=int_args_test,
    #         key_property=int_generator_test
    #     )
    #     assert len(nodes) == 1
    #     assert nodes.get("n1") == expectedNodeMapping

    # def test_mapping_from_json(self):

