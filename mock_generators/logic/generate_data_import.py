from models.mapping import Mapping
from models.data_import import DataImporterJson
from file_utils import save_json

def generate_data_importer_json(
    mapping: Mapping,
    export_folder: str):
    # Will generate .csvs and a .json file for use with Neo4j's data-importer. Returns filename of .csv file

    # MUST be run AFTER nodes and relationships have generated their
    # mock data, as the data-importer needs this info to generate the
    # schemas
    
    dij = DataImporterJson()

    # Generate nodes
    nodes = mapping.nodes
    dij.add_nodes(nodes)

    # Generate relationships
    relationships = mapping.relationships
    dij.add_relationships(relationships)

    # Generate data-importer json
    # The data-import json file is a dict made up of 4 keys:
    export_path = f"{export_folder}/neo4j_importer_model.json"
    save_json(export_path, dij.to_dict())