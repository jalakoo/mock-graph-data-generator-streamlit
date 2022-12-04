from models.mapping import Mapping, NodeMapping, RelationshipMapping, PropertyMapping
from models.generator import Generator
import logging
from file_utils import load_string
import sys

def generate_cypher(
    mapping: Mapping,
    export_folder: str):

    # Will generate cypher commands to add mock data in a Neo4j's database via a browser interface.

    logging.info('tbd')