from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
from models.data_import_json import DataImporterJson
import logging
from logic.generate_csv_nodes import generate_csv_nodes

# def generate_node_csv_header(node: NodeMapping)->list[str]:
#     # Generate a column header and value for every property in the node
#     properties: PropertyMapping = node.properties
#     result = ["id"]
#     logging.info(f'generate_node_csv_header: {node.caption} properties: {properties}')
#     for property in properties:
#         result.append(property.name)
#     return result

# def generate_node_csv(node: NodeMapping)->list[any]:
#     # Generate values for properties
#     properties: PropertyMapping = node.properties
#     result = [f'{node.id}'] 
#     for property in properties:
#         args = property.generator_args
#         value = property.generator.run(args)
#         logging.info(f'generate_node_csv: {property.name} = {value}')
#         result.append(value)
#     return result

def generate_csv(
    mapping: Mapping,
    export_folder: str):
    
    # Will generate .csvs and a .json file for use with Neo4j's data-importer
    
    # Generate nodes
    nodes = mapping.nodes
    generate_csv_nodes(nodes, export_folder)
    # for node_id, node in nodes.items():
    #     logging.info(f"Generating node: {node}")

    #     # csv filename to save node data to
    #     csv_filename = f"{node.caption}_{node_id}.csv"
    #     # remove trailing slash if present
    #     cleaned_export_folder = export_folder.rstrip("/") 
    #     csv_filepath = f"{cleaned_export_folder}/{csv_filename}"


    #     #  Determine how many nodes to generate
    #     count_generator = node.count_generator
    #     count_generator_args = node.count_generator_args
    #     count = None
    #     try:
    #         code_filepath = count_generator.code_url
    #         module = __import__(count_generator.import_url(), fromlist=['generate'])
    #         count = module.generate(count_generator_args)
    #         logging.info(f'Generating {count} nodes')
    #     except:
    #         logging.error(f"Could not load count_generator code from {code_filepath}: {sys.exc_info()[0]}")
    #         continue

    #     # Generate nodes with properties
    #     if count is not None:
    #         # Generate .csv header
    #         header = generate_node_csv_header(node)
    #         rows = []
    #         # Generate row data
    #         for _ in range(count):
    #             rows.append(generate_node_csv(node))
            
    #         logging.info(f'header: {header}, rows: {rows}')
    #         # Save source .csv
    #         save_csv(filepath=csv_filepath, header=header, data=rows)

    #         # Generate dataModel:fileModel:fileSchemas entry



    # Generate relationships
    # logging.info('tbd')

    # Generate data-importer json
    # The data-import json file is a dict made up of 4 keys:
    # version, graph, dataModel, and graphModel

    # Current version this schema applies to is "version": "0.5.2",

    # The graph key looks like:
    # "graph": {
    #   "nodes": [
    #     {
    #       "id": "n0",
    #       "position": {
    #         "x": -120,
    #         "y": 98
    #       },
    #       "caption": "Comm"
    #     },
    #     {
    #       "id": "n1",
    #       "position": {
    #         "x": 146,
    #         "y": -112.5
    #       },
    #       "caption": "Project"
    #     }
    #   ],
    #   "relationships": [
    #     {
    #       "id": "n0",
    #       "type": "ASSOCIATED_WITH",
    #       "fromId": "n0",
    #       "toId": "n1"
    #     },
    #     {
    #       "id": "n1",
    #       "type": "REPORTS_TO",
    #       "fromId": "n2",
    #       "toId": "n2"
    #     }
    #   ]
    # }

    # TODO: Due the ids need to be n# format?
    # Hopefully can any unique id for ids will work
    # positions can be carried over from the arrows mapping, but converted from floats -> ints
    # Take only the first label and use as caption?


    # The dataModel looks like:
    # "dataModel": {
    #   "fileModel": {
    #     "fileSchemas": {
    #       "commsTo.csv": {
    #         "expanded": true,
    #         "fields": [
    #           {
    #             "name": "comm_id",
    #             "type": "string",
    #             "sample": "8e26270b-3535-4c9b-8048-1864a394df99",
    #             "include": true
    #           },
    #           {
    #             "name": "sent_to",
    #             "type": "string",
    #             "sample": "0485822c-ae1a-4695-bbb3-b5f3d982af53",
    #             "include": true
    #           }
    #         ]
    #       }
    #     }
    #   }
    # }

    #  TODO: generate .csv per node, relationship, and node-relationship types


    # The graphModel looks like:
    # "graphModel": {
    #     "nodeSchemas": {
    #       "n0": {
    #         "label": "Comm",
    #         "additionLabels": [],
    #         "labelProperties": [],
    #         "properties": [
    #           {
    #             "property": "comm_id",
    #             "type": "string",
    #             "identifier": "n4MV672Jo5105gOJOXgME"
    #           },
    #           {
    #             "property": "type",
    #             "type": "string",
    #             "identifier": "5b7V-ytLydos3oOr61deU"
    #           },
    #           {
    #             "property": "created_at",
    #             "type": "string",
    #             "identifier": "iPKRcqe61csGPoeHOAvkk"
    #           }
    #         ],
    #         "key": {
    #           "properties": [
    #             "n4MV672Jo5105gOJOXgME"
    #           ],
    #           "name": ""
    #         }
    #       }
    #     },
    #     "relationshipSchemas": {
    #       "n0": {
    #         "type": "ASSOCIATED_WITH",
    #         "sourceNodeSchema": "n0",
    #         "targetNodeSchema": "n1",
    #         "properties": []
    #       },
    #       "n1": {
    #         "type": "REPORTS_TO",
    #         "sourceNodeSchema": "n2",
    #         "targetNodeSchema": "n2",
    #         "properties": []
    #       },
    #   },
    #   "mappingModel": {
    #     "nodeMappings": {
    #       "n0": {
    #         "nodeSchema": "n0",
    #         "fileSchema": "comms.csv",
    #         "mappings": [
    #           {
    #             "field": "comm_id"
    #           },
    #           {
    #             "field": "type"
    #           },
    #           {
    #             "field": "created_at"
    #           }
    #         ]
    #       },
    #     },
    #     "relationshipMappings": {
    #       "n0": {
    #         "relationshipSchema": "n0",
    #         "mappings": [],
    #         "sourceMappings": [
    #           {
    #             "field": "comm_id"
    #           }
    #         ],
    #         "targetMappings": [
    #           {
    #             "field": "project_id"
    #           }
    #         ],
    #         "fileSchema": "comms.csv"
    #       },
    #       "n1": {
    #         "relationshipSchema": "n1",
    #         "mappings": [],
    #         "sourceMappings": [
    #           {
    #             "field": "employee_id"
    #           }
    #         ],
    #         "targetMappings": [
    #           {
    #             "field": "reports_to"
    #           }
    #         ],
    #         "fileSchema": "people.csv"
    #       }
    #   },
    #   "configurations": {
    #     "idsToIgnore": []
    #   }
    # }

    # TODO: node schemas MUST specify the property that will act as a key

    # TODO: Need sample of relationship properties info

    # mappingModel: nodeMappings look straightforward, high level node info
    # mappingModel: relationshipMappings refer to a particular relationshipSchema id from the graphModel