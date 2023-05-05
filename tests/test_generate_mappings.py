import os
import pytest

from mock_generators.models.generator import Generator, GeneratorType
import json
import logging

# test_generators = load_generators("mock_generators/named_generators.json")

# TODO: Test propertymappings_for_raw_properties
# TODO: Test node_mappings_from
# TODO: Test relationshipmappings_from
# TODO: Test mapping_from_json
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

    # def test_failed_generator_for_raw_property(self):
    #     try:
    #         generator, args = generator_for_raw_property("{\'test_doesnt_exist\':[1]}", test_generators)
    #         assert generator is None
    #         assert args is None
    #     except Exception as e:
    #         print(f'Exception: {e}')


    # def test_propertymappings_for_raw_properties_smoke(self):
    #     raw_props = {
    #             "alpha": "{\"test_int\":[1]}",
    #             "bravo": "{\"test_float\":[1.0, 2.0]}"
    #         }
    #     mappings = propertymappings_for_raw_properties(
    #         raw_properties=raw_props,
    #         generators= test_generators)
    #     assert len(mappings) == 2

    # def test_node_mappings_from_literals(self):
    #     nodes = [
    #         {
    #             "id": "n1",
    #             "position": {
    #             "x": 284.5,
    #             "y": -204
    #             },
    #             "caption": "Company",
    #             "labels": [],
    #             "properties": {
    #                 "string": "name",
    #                 "bool": "bool",
    #                 "int": "int",
    #                 "float": "float",
    #                 "datetime": "2020-01-01T00:00:00Z"
    #             },
    #             "style": {}
    #         }
    #     ]

    # def test_propertymappings_for_raw_properties_literals(self):
    #     raw_props = {
    #             "string": "test",
    #             "bool": True,
    #             "int": 1,
    #             "float": 1.0,
    #             "datetime": "2020-01-01T00:00:00Z",
    #     }
    #     mappings = propertymappings_for_raw_properties(
    #         raw_properties=raw_props,
    #         generators= test_generators)
        
    #     assert len(mappings) == 5
    #     assert mappings["string"] == "test"
    #     assert mappings["bool"] == True
    #     assert mappings["int"] == 1
    #     assert mappings["float"] == 1.0
    #     assert mappings["datetime"] == "2020-01-01T00:00:00Z"



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

