from models.mapping import Mapping
from models.data_import import DataImporterJson
from file_utils import save_json
import logging
import sys

def generate_data_importer_json(
    mapping: Mapping,
    export_folder: str,
    export_filename: str) -> bool:
    # Returns True if files generated, False if not

    # Will generate .csvs and a .json file for use with Neo4j's data-importer. Returns filename of .csv file

    # MUST be run AFTER nodes and relationships have generated their
    # mock data, as the data-importer needs this info to generate the
    # schemas
    
    dij = DataImporterJson()

    try:
        # Generate nodes
        nodes = mapping.nodes
        dij.add_nodes(nodes)
    except:
        raise Exception(f'Error adding nodes for data-importer json: {sys.exc_info()[0]}')

    try:
        # Generate relationships
        relationships = mapping.relationships
        dij.add_relationships(relationships)
    except:
        raise Exception(f'Error adding relationships for data-importer json: {sys.exc_info()[0]}')

    # TODO: Verify format of exported .json file

    try:
        # Generate data-importer json
        # The data-import json file is a dict made up of 4 keys:
        export_path = f"{export_folder}/{export_filename}.json"
        dij_dict = dij.to_dict()
        save_json(export_path, dij_dict)
        return True
    except:
        logging.error(f'Unable to export data-importer json file to export folder: {export_folder}\n\ndata-import object: {dij_dict}\n\nError: {sys.exc_info()[0]}')
        return False