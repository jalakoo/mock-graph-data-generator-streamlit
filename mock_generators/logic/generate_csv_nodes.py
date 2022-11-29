from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
from models.data_import import DataImporterJson
import logging

def generate_node_csv_header(node: NodeMapping)->list[str]:
    # Generate column headers for node .csv
    properties: PropertyMapping = node.properties
    result = []
    for property in properties:
        result.append(property.name)
    return result

def generate_node_csv(node: NodeMapping)->list[any]:
    # Generate .csv rows
    properties: PropertyMapping = node.properties
    result = [] 
    for property in properties:
        args = property.args
        value = property.generator.generate(args)
        result.append(value)
    return result

def generate_csv_node(
    node: NodeMapping, 
    export_folder: str):

    logging.info(f"Generating node: {node}")

    # csv filename to save node data to
    csv_filename = f"{node.filename()}.csv"
    # remove trailing slash if present
    cleaned_export_folder = export_folder.rstrip("/") 
    csv_filepath = f"{cleaned_export_folder}/{csv_filename}"


    #  Determine how many nodes to generate
    count_generator = node.count_generator
    count_args = node.count_args
    count = None
    try:
        code_filepath = count_generator.code_url
        module = __import__(count_generator.import_url(), fromlist=['generate'])
        count = module.generate(count_args)
        # logging.info(f'Generating {count} nodes')
    except:
        logging.error(f"Could not load count_generator code from {code_filepath}: {sys.exc_info()[0]}")
        return

    # Generate nodes with properties
    if count is not None:
        # Generate .csv header
        header = generate_node_csv_header(node)
        rows = []
        # Generate row data
        for _ in range(count):
            rows.append(generate_node_csv(node))
        
        # logging.info(f'header: {header}, rows: {rows}')
        # Save source .csv
        save_csv(filepath=csv_filepath, header=header, data=rows)


def generate_csv_nodes(
    nodes: dict[str, NodeMapping],
    export_folder: str):
    for key, node in nodes.items():
        generate_csv_node(node, export_folder)