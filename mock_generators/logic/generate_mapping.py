# Builds mapping file from specially formatted arrows.app JSON file

import json
from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.generator import Generator
import logging

def generator_for_raw_property(
    property_value: str, 
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """Returns a generator and args for a property"""
    # Check that the property info is notated for mock data generation use
    leading_bracket = property_value[0]
    trailing_bracket = property_value[-1]
    if leading_bracket != "{" or trailing_bracket != "}":
        logging.warning(f'generate_mapping.py: generator_for_raw_property: property_value not wrapped in {{ and }}. Skipping generator assignment for property_value: {property_value}')
        return (None, None)
    
    # The property value should be a JSON string. Convert to a dict obj
    json_string = property_value[1:-2]
    obj = json.loads(json_string)
    
    # Should only ever be one
    for key, value in obj.items():
        generator_id = key
        generator = generators.get(generator_id, None)
        if generator is None:
            logging.error(f'generate_mapping.py: generator_for_raw_property: generator_id {generator_id} not found in generators. Skipping generator assignment for property_value: {property_value}')
            return None

        args = value
        return (generator, args)

def node_mappings_from(
    node_dicts: list,
    generators: dict[str, Generator]
    ) -> list[NodeMapping]:
    """Converts node information from JSON file to mapping objects"""
    # Sample node_dict
    # {
    #     "id": "n1",
    #     "position": {
    #       "x": 284.5,
    #       "y": -204
    #     },
    #     "caption": "Company",
    #     "labels": [],
    #     "properties": {
    #       "name": "{{\"company_name\":[]}}",
    #       "uuid": "{{\"uuid\":[8]}}",
    #       "{{count}}": "{{\"int\":[1]}}",
    #       "{{key}}": "uuid"
    #     },
    #     "style": {}
    #   }

    node_mappings = []
    for node_dict in node_dicts:

        # Check for required properties dict
        properties = node_dict.get("properties", None)
        if properties is None:
            logging.warning(f"generate_mappings: node_mappings_from: dict is missing properties: {node_dict}. Can not configure for data generation. Skipping node.")
            continue

        # Determine count generator to use
        count_generator_config = properties.get("{{count}}", None)
        if count_generator_config is not None:
            logging.warning(f"generate_mappings: node_mappings_from: node properties is missing {{count key}}: Skipping {node_dict}")
            continue

        key = properties.get("{{key}}", None)
        if key is not None:
            logging.warning(f"generate_mappings: node_mappings_from: node properties is missing {{key}}: Skipping {node_dict}")
            continue

        # Get proper generators for count generator
        count_generator, count_args = generator_for_raw_property(count_generator_config, generators)

        # TODO:
        # Create property mappings for properties

        # Assign correct property mapping as key property

        # Create node mapping
        node_mapping = NodeMapping(
            nid = node_dict["id"],
            label = node_dict["label"],
            properties = node_dict["properties"],
            count_generator=count_generator,
            count_args=count_args,
        )
        # TODO:
        # Run generators
        node_mappings.append(node_mapping)
    return node_mappings


def mapping_from_json(json_file: str) -> Mapping:

    # Validate json file
    loaded_json = json.loads(json_file)

    # Check required elements needed
    node_dicts = loaded_json.get("nodes", None)
    if node_dicts is None:
        raise Exception(f"generate_mappings: mapping_from_json: No nodes found in JSON file: {json}")
    relationship_dicts = loaded_json.get("relationships", None)
    if relationship_dicts is None:
        raise Exception(f"generate_mappings: mapping_from_json: No relationships found in JSON file: {json}")

    # Convert source information to mapping objects
    nodes = node_mappings_from(node_dicts)

    # Create mapping object


    # return mapping