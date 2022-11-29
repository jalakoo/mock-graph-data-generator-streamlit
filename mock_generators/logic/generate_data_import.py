from models.mapping import Mapping
from models.data_import import DataImporterJson
from file_utils import save_json

def generate_data_importer_json(
    mapping: Mapping,
    export_folder: str):
    # Will generate .csvs and a .json file for use with Neo4j's data-importer. Returns filename of .csv file
    
    dij = DataImporterJson()

    # Generate nodes
    nodes = mapping.nodes
    dij.add_nodes(nodes)

    # Generate relationships
    relationships = mapping.relationships
    dij.add_relationships(relationships)

    # Generate data-importer json
    # The data-import json file is a dict made up of 4 keys:
    export_path = f"{export_folder}/data_import.json"
    save_json(export_path, dij.to_dict())