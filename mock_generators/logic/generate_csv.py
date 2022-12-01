from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
import logging
from logic.generate_csv_nodes import generate_csv_node
from logic.generate_data_import import generate_data_importer_json

def generate_csv(
    mapping: Mapping,
    export_folder: str):
    
    # Generate node values
    #  Determine how many nodes to generate
    for _, node in mapping.nodes.items():
        values : list[dict] = node.generate_values()
        generate_csv_node(f'{node.filename()}.csv', values, export_folder)

    # Generate relationships, or more accurately, the csv files that
    # the data-importer will use to know which created nodes are connected
    # generate_csv_relationships(mapping.relationships, export_folder)