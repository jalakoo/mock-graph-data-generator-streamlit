# Builds mapping file from specially formatted arrows.app JSON file

import json
from .models.mapping import Mapping
from .models.node_mapping import NodeMapping
from .models.relationship_mapping import RelationshipMapping
from .models.property_mapping import PropertyMapping
from .models.generator import Generator
import logging
import uuid

def generator_for_raw_property(
    property_value: str, 
    generators: dict[str, Generator]
    ) -> tuple[Generator, list[any]]:
    """Returns a generator and args for a property"""
    # Sample expected string: "{\"company_name\":[]}"

    try:
        obj = json.loads(property_value)
    except Exception as e:
        logging.info(f'Could not parse JSON string: {property_value}. Skipping generator assignment for property_value: {property_value}')
        return (None, None)

    # Should only ever be one
    for key, value in obj.items():
        generator_id = key
        generator = generators.get(generator_id, None)
        if generator is None:
            logging.error(f'Generator_id {generator_id} not found in generators. Skipping generator assignment for property_value: {property_value}')
            return None

        args = value
        return (generator, args)

def propertymappings_for_raw_properties(
    raw_properties: dict[str, str], 
    generators: dict[str, Generator]
    ) -> dict[str, PropertyMapping]:
    """Returns a list of property mappings for a node or relationship"""
    property_mappings = {}
    for key, value in raw_properties.items():
        generator, args = generator_for_raw_property(value, generators)
        if generator is None:
            # TODO: Insert PropertyMapping with no generator? Use literal value?
            continue

        pid = str(uuid.uuid4())[:8]
        property_mapping = PropertyMapping(
            pid = pid,
            name=key,
            generator=generator,
            args=args
        )
        property_mappings[pid] = property_mapping
    return property_mappings

def node_mappings_from(
    node_dicts: list,
    generators: dict[str, Generator]
    ) -> dict[str, NodeMapping]:
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

    node_mappings = {}
    for node_dict in node_dicts:

        # Check for required data in raw node dict from arrows.app json
        position = node_dict.get("position", None)
        if position is None:
            logging.warning(f"generate_mappings: node_mappings_from: node properties is missing position key from: {node_dict}: Skipping {node_dict}")
            continue

        caption = node_dict.get("caption", None)
        if caption is None:
            logging.warning(f"generate_mappings: node_mappings_from: node properties is missing caption key from: {node_dict}: Skipping {node_dict}")
            continue


        # Check for required properties dict
        properties = node_dict.get("properties", None)
        if properties is None:
            logging.warning(f"generate_mappings: node_mappings_from: dict is missing properties: {node_dict}. Can not configure for data generation. Skipping node.")
            continue

        # Determine count generator to use
        count_generator_config = properties.get("{count}", None)
        if count_generator_config is None:
            logging.warning(f"generate_mappings: node_mappings_from: node properties is missing {{count}} key from properties: {properties}: Skipping {node_dict}")
            continue

        # Get string name for key property. Value should be an unformatted string
        key = properties.get("{key}", None)
        if key is None:
            logging.warning(f"generate_mappings: node_mappings_from: node properties is missing {{key}}: Skipping {node_dict}")
            continue

        # Get proper generators for count generator
        count_generator, count_args = generator_for_raw_property(count_generator_config, generators)

        # Create property mappings for properties
        property_mappings = propertymappings_for_raw_properties(properties, generators)

        # Assign correct property mapping as key property
        # logging.info(f'generate_mappings: node_mappings_from: key_property: {key}, property_mappings: {property_mappings}')
        key_property = next((v for k,v in property_mappings.items() if v.name == key), None)
        if key_property is None:
            logging.warning(f"generate_mappings: node_mappings_from: No key property mapping found for node: {node_dict} - key name: {key}. Skipping node.")
            continue

        # Create node mapping
        node_mapping = NodeMapping(
            nid = node_dict["id"],
            labels = node_dict["labels"],
            properties = property_mappings,
            count_generator=count_generator,
            count_args=count_args,
            key_property=key_property,
            position = position,
            caption=caption
        )
        # TODO:
        # Run generators
        node_mappings[node_mapping.nid] = node_mapping
    return node_mappings

def relationshipmappings_from(
    relationship_dicts: list[dict],
    nodes: dict[str, NodeMapping],
    generators: dict[str, Generator]
    ) -> dict[str,RelationshipMapping]:
    # Sample relationship_dict
    # {
    #     "id": "n0",
    #     "fromId": "n1",
    #     "toId": "n0",
    #     "type": "EMPLOYS",
    #     "properties": {
    #       "{count}": "{\"int\":[10]}",
    #       "{assignment}": "{\"exhaustive_random\":[]}",
    #       "{filter}": "{string_from_list:[]}"
    #     },
    #     "style": {}
    #   },
    relationshipmappings = {}
    for relationship_dict in relationship_dicts:
        # Check for required data in raw node dict from arrows.app json

        rid = relationship_dict.get("id", None)
        if rid is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: relationship properties is missing 'id' key from: {relationship_dict}: Skipping {relationship_dict}")
            continue
        type = relationship_dict.get("type", None)
        if type is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: relationship properties is missing 'type' key from: {relationship_dict}: Skipping {relationship_dict}")
            continue
        from_id = relationship_dict.get("fromId", None)
        if from_id is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: relationship properties is missing 'fromId' key from: {relationship_dict}: Skipping {relationship_dict}")
            continue

        to_id = relationship_dict.get("toId", None)
        if to_id is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: relationship properties is missing 'toId' key from: {relationship_dict}: Skipping {relationship_dict}")
            continue

        # Check for required properties dict
        properties = relationship_dict.get("properties", None)
        if properties is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: dict is missing properties: {relationship_dict}. Can not configure for data generation. Skipping relationship.")
            continue

        # Determine count generator to use
        count_generator_config = properties.get("{count}", None)
        if count_generator_config is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: relationship properties is missing '{{count}}' key from properties: {properties}: Skipping {relationship_dict}")
            continue

        assignment_generator_config = properties.get("{assignment}", None)
        # If missing, use ExhaustiveRandom
        if assignment_generator_config is None:
            assignment_generator_config = "{\"exhaustive_random\":[]}"

        # Get proper generators for count generator
        count_generator, count_args = generator_for_raw_property(count_generator_config, generators)

        # Create property mappings for properties
        property_mappings = propertymappings_for_raw_properties(properties, generators)

        assignment_generator, assignment_args = generator_for_raw_property(assignment_generator_config, generators)

        from_node = nodes.get(from_id, None)
        if from_node is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: No node mapping found for relationship: {relationship_dict} - fromId: {from_id}. Skipping relationship.")
            continue

        to_node = nodes.get(to_id, None)
        if to_node is None:
            logging.warning(f"generate_mappings: relationshipmappings_from: No node mapping found for relationship: {relationship_dict} - toId: {to_id}. Skipping relationship.")
            continue

        # Create relationship mapping
        relationship_mapping = RelationshipMapping(
            rid = rid,
            type = type,
            from_node = from_node,
            to_node = to_node ,
            count_generator=count_generator,
            count_args=count_args,
            properties=property_mappings,
            assignment_generator= assignment_generator,
            assignment_args=assignment_args
        )
        relationshipmappings[relationship_mapping.rid] = relationship_mapping

    return relationshipmappings


def mapping_from_json(
    json_file: str,
    generators: list[Generator]) -> Mapping:

    try:
        # Validate json file
        loaded_json = json.loads(json_file)
    except Exception as e:
        raise Exception(f"generate_mappings: mapping_from_json: Error loading JSON file: {e}")

    # Extract and process nodes
    node_dicts = loaded_json.get("nodes", None)
    if node_dicts is None:
        raise Exception(f"generate_mappings: mapping_from_json: No nodes found in JSON file: {json}")
    relationship_dicts = loaded_json.get("relationships", None)
    if relationship_dicts is None:
        raise Exception(f"generate_mappings: mapping_from_json: No relationships found in JSON file: {json}")

    # Convert source information to mapping objects
    nodes = node_mappings_from(node_dicts, generators)
    relationships = relationshipmappings_from(relationship_dicts, nodes, generators)

    # Create mapping object
    mapping = Mapping(
        nodes=nodes,
        relationships=relationships
    )
    return mapping
