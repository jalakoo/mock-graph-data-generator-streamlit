from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
import logging
from logic.generate_csv_nodes import generate_csv_nodes
from logic.generate_data_import import generate_data_importer_json

def generate_csv(
    mapping: Mapping,
    export_folder: str):
    
    # Will generate .csvs and a .json file for use with Neo4j's data-importer. Returns filename of .csv file
    
    # Generate nodes
    nodes = mapping.nodes
    generate_csv_nodes(nodes, export_folder)

    # Generate relationships
    # logging.info('tbd')

    # Generate data-importer json
    # The data-import json file is a dict made up of 4 keys:
    # version, graph, dataModel, and graphModel. See the samples/data_import.json file for reference.
    generate_data_importer_json(mapping, export_folder)

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