# Builds mapping file from specially formatted arrows.app JSON file

import json
from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
from logic.generate_values import generator_for_raw_property, actual_generator_for_raw_property, assignment_generator_for
import logging
import uuid


def generate_addresses_to(
    raw_properties: dict[str, str],
    generators: dict[str, Generator]):

    # Insert all values - they will be read as literals during the node generation process
    raw_properties['street'] = f'{{"street":[]}}'
    raw_properties['city'] = f'{{"city":[]}}'
    raw_properties['state'] = f'{{"state":[]}}'
    raw_properties['zip'] = f'{{"postcode":[]}}'
    raw_properties['country'] = f'{{"country":[]}}'
    return raw_properties

def xgenerate_addresses_to(
    raw_properties: dict[str, str],
    generators: dict[str, Generator]):

    generator, args = actual_generator_for_raw_property('{"address_usa": []}', generators)
    value = generator.generate(args)
    # Insert all values - they will be read as literals during the node generation process
    try:
        address1 = value.get('address1', None)
        if address1 is not None:
            raw_properties['address1'] = f'{{"string":["{address1}"]}}'
        address2 = value.get('address2', None)
        if address2 is not None:
            raw_properties['address2'] = f'{{"string":["{address2}"]}}'
        city = value.get('city', None)
        if city is not None:
            raw_properties['city'] = f'{{"string":["{city}"]}}'
        state = value.get('state', None)
        if state is not None:
            raw_properties['state'] = f'{{"string":["{state}"]}}'
        postalCode = value.get('postalCode', None)
        if postalCode is not None:
            raw_properties['postalCode'] = f'{{"string":["{postalCode}"]}}'
        lat = value.get('coordinates', None).get('lat', None)
        if lat is not None:
            raw_properties['latitude'] = f'{{"string":["{lat}"]}}'
        lng = value.get('coordinates', None).get('lng', None)
        if lng is not None:
            raw_properties['longitude'] = f'{{"string":["{lng}"]}}'
        # Add country
        raw_properties['country'] = f'{{"string":["USA"]}}'
    except Exception as e:
        logging.error(f'Problem extracting data from address object: {value}: ERROR: {e}')
    
    return raw_properties


def propertymappings_for_raw_properties(
    raw_properties: dict[str, str], 
    generators: dict[str, Generator]
    ) -> dict[str, PropertyMapping]:
    """Returns a list of property mappings for a node or relationship"""

    # raw_properties is a dict of key value pairs from properties value from an entry from the arrows.app JSON file. Example:
    # {
    #     "name": "{\"company_name\":[]}",
    #     "uuid": "{\"uuid\":[8]}",
    #     "{count}": "{\"int\":[1]}",
    #     "{key}": "uuid"
    # },  

    property_mappings = {}
    
    if generators is None or len(generators) == 0:
        raise Exception(f'generate_mapping.py: propertymappings_for_raw_properties: No generators assignment received.')

    # Special handling for addresses
    raw_keys = raw_properties.keys()
    # Assign uuid if not key property assignment was made
    if "{key}" not in raw_keys and "KEY" not in raw_keys:
        raw_properties["KEY"] = "_uid"
        raw_properties["_uid"] = f'{{"uuid":[]}}'
    if "ADDRESS" in raw_keys:
        raw_properties.pop("ADDRESS")
        raw_properties = generate_addresses_to(raw_properties, generators)

    for key, value in raw_properties.items():

        # Skip any keys with { } (brackets) as these are special cases for defining count/assignment/filter generators
        if key.startswith('{') and key.endswith('}'):
            continue

        # Skip special COUNT and KEY literals
        if key == "COUNT" or key == "KEY":
                continue

        try:
            generator, args = generator_for_raw_property(value, generators)
            if generator is None:
                # TODO: Insert PropertyMapping with no generator? Use literal value?
                logging.warning(f'generate_mapping.py: propertymappings_for_raw_properties: could not find generator for key: {key}, property_value: {value}')
                continue

            # pid = str(uuid.uuid4())[:8]
            pid = key
            property_mapping = PropertyMapping(
                pid = pid,
                name=key,
                generator=generator,
                args=args
            )
            property_mappings[pid] = property_mapping
        except Exception as e:
            logging.warning(f'generate_mapping.py: propertymappings_for_raw_properties: could not create property mapping for key: {key}, property_value: {value}: {e}')
            continue
    return property_mappings

def node_mappings_from(
    node_dicts: list,
    generators: dict[str, Generator]
    ) -> dict[str, NodeMapping]:
    """Converts node information from arrows JSON file to mapping objects"""
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
    #       "name": "{\"company_name\":[]}",
    #       "uuid": "{\"uuid\":[8]}}",
    #       "{count}": "{{"int\":[1]}",
    #       "{key}": "uuid"
    #     },
    #     "style": {}
    #   }

    # Prepare a dict to store mappings. Incoming node id to be keys
    node_mappings = {}

    # Process each incoming node data
    for node_dict in node_dicts:

        # Incoming data validation
        position = node_dict.get("position", None)
        if position is None:
            logging.warning(f"Node properties is missing position key from: {node_dict}: Skipping {node_dict}")
            continue

        caption = node_dict.get("caption", None)
        if caption is None:
            logging.warning(f"Node properties is missing caption key from: {node_dict}: Skipping {node_dict}")
            continue

        # Check for optional properties dict
        properties = node_dict.get("properties", {})
        # Always add a _uid property to node properties
        properties["_uid"] = "{\"uuid\":[]}"

        # Create property mappings for properties
        try: 
            property_mappings = propertymappings_for_raw_properties(properties, generators)
        except Exception as e:
            logging.warning(f"Could not create property mappings for node: {node_dict}: {e}")
            continue

        # Determine count generator to use
        # TODO: Support COUNT literal
        count_generator_config = properties.get("COUNT", None)
        if count_generator_config is None:
            count_generator_config = properties.get("{count}", None)
            if count_generator_config is None:
                count_generator_config = '{"int_range": [1,100]}'
                logging.info(f"node properties is missing COUNT or {{count}} key from properties: {properties}: Using defalt int_range generator")

        # Get proper generators for count generator
        try:
            count_generator, count_args = generator_for_raw_property(count_generator_config, generators)
        except Exception as e:
            logging.warning(f"Could not find count generator for node: {node_dict}: {e}")
            continue

        # Get string name for key property. Value should be an unformatted string
        key = properties.get("KEY", None)
        if key is None:
            key = properties.get("{key}", None)
            if key is None:
                key = "_uid"
                logging.info(f"node properties is missing KEY or {{key}}: Assigning self generated _uid")

        # Assign correct property mapping as key property
        key_property = next((v for k,v in property_mappings.items() if v.name == key), None)
        if key_property is None:
            logging.warning(f"Key property mapping not found for node: {node_dict} - key name: {key}. Skipping node.")
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
        properties = relationship_dict.get("properties", {})

        # Determine count generator to use
        # TODO: Support COUNT key type
        count_generator_config = properties.get("COUNT", None)
        if count_generator_config is None:
            count_generator_config = properties.get("{count}", None)
            if count_generator_config is None:
                count_generator_config = '{"int_range": [1,3]}'
                logging.info(f"Relationship properties is missing COUNT or '{{count}}' key from properties: {properties}: Using default int_range generator")

        assignment_generator_config = properties.get("ASSIGNMENT", None)
        if assignment_generator_config is None:
            assignment_generator_config = properties.get("{assignment}", None)
            # If missing, use ExhaustiveRandom
            if assignment_generator_config is None:
                assignment_generator_config = "{\"exhaustive_random\":[]}"

        # Get proper generators for count generator
        try:
            count_generator, count_args = generator_for_raw_property(count_generator_config, generators)
        except Exception as e:
            logging.warning(f"generate_mappings: relationshipmappings_from: could not find count generator for relationship: {relationship_dict}: {e}")
            continue

        # Create property mappings for properties
        try:
            property_mappings = propertymappings_for_raw_properties(properties, generators)
        except Exception as e:
            logging.warning(f"generate_mappings: relationshipmappings_from: could not create property mappings for relationship: {relationship_dict}: {e}")
            continue

        try:
            assignment_generator, assignment_args = assignment_generator_for(assignment_generator_config, generators)
        except Exception as e:
            logging.warning(f"generate_mappings: relationshipmappings_from: could not get assignment generator for relationship: {relationship_dict}: {e}")
            continue

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

    # TODO:
    # Purge orphaned nodes

    # Convert source information to mapping objects
    nodes = node_mappings_from(node_dicts, generators)
    relationships = relationshipmappings_from(relationship_dicts, nodes, generators)

    # Create mapping object
    mapping = Mapping(
        nodes=nodes,
        relationships=relationships
    )
    return mapping
