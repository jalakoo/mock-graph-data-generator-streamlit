from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
import logging
from logic.generate_csv_nodes import export_csv_node
from logic.generate_csv_relationships import export_csv_relationship
from logic.generate_data_import import generate_data_importer_json

def generate_csv(
    mapping: Mapping,
    export_folder: str) -> bool:
    # Returns True if files generated, False if not
    
    # For storing all generated value from each node type
    all_node_values : dict[str, list[dict]] = {}
    
    # Generate node values    
    for uid, node in mapping.nodes.items():
        # Each nodeMapping is capable of generating and retaining it's own mock list data
        values : list[dict] = node.generate_values()
        if values is None or values == []:
            logging.warning(f'No values generated for node {node.caption}')
            return False

        export_csv_node(f'{node.filename()}.csv', values, export_folder)

        #  Retain for use with relationships
        all_node_values[uid] = values


    if all_node_values == {}:
        logging.warning('No node values generated. No relationships will be generated.')
        return False
    # Generate relationships, or more accurately, the csv files that
    # the data-importer will use to know which created nodes are connected with the mapped relationships
    for uid, relationship in mapping.relationships.items():
        # Each relationship mapping is capable of generating and storing it's own list of mock list data, dependent on previously generated node values
        # logging.info(f'Generating values for relationship {relationship}: all nodes: {all_node_values}')
        r_values : list[dict] = relationship.generate_values(all_node_values)
        logging.info(f'r_values: {r_values}')
        export_csv_relationship(f'{relationship.filename()}.csv', r_values, export_folder)

    return True