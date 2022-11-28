from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
import logging

class DataImporterJson():
    def __init__(self, version: str = "0.5.2"):
        self.dict = {
            "version": version,
            "graph":{
                "nodes":[],
                "relationships":[]
            },
            "dataModel":{
                "fileModel":{
                    "fileSchemas":{

                    }
                },
                "graphModel":{
                    "nodeSchemas":{

                    },
                    "relationshipSchemas":{
                    }
                },
                "mappingModel":{
                    "nodeMappings":{
                    },
                    "relationshipMappings":{
                    }
                },
                "configuration":{
                    "idsToIgnore":[],
                }
            }
        }

    def add_node(
        self,
        node: NodeMapping,
        csv_filename: str
        ):

        caption = node.get("caption", None)
        if caption is None:
            logging.error(f"Node {node} does not have a caption")

        # Add to graph:nodes
        self.data["graph"]["nodes"].append({
            "id": node.id,
            "position": node.position,
            "caption": caption
        })

        # TODO: Add .csv file origin and reference info in dataModel:fileModel:fileSchemas

        # TODO: Add to graphModel:nodeSchemas
        # TODO: Examples of labelProperties

        # TODO: Add to graphModel:mappingModel:nodeMappings
