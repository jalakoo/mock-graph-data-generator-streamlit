from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
import logging


def file_schema_node_property(property: PropertyMapping)-> dict:
    sample_value = property.generator.generate(property.args)
    result = {
        "name": property.name,
        "type": property.type.to_string().lower(),
        "sample": sample_value,
        "include": True
    }
    return result

def file_schema_node(node: NodeMapping) -> dict:
    result = {
        f"{node.filename()}.csv":{
            "expanded": True,
            "fields":[
                file_schema_node_property(property) for property in node.properties
            ]
        }
    }
    return result


def graph_model_relationship_property(property: PropertyMapping)-> dict:
    result = {
        "property": property.name,
        "type": property.type.to_string().lower(),
        "identifier": property.id
        }
    return result

# def graph_model_relationship(relationship: RelationshipMapping) -> dict:
#     result = {
#         f"{relationship.id}":{
#             "type": relationship.type,
#             "sourceNodeSchema": relationship.start_node_id,
#             "targetNodeSchema": relationship.end_node_id,
#             "properties":[
#                 file_schema_node_property(property) for property in relationship.properties
#             ]
#         }
#     }
#     return result

class DataImporterJson():
    def __init__(self, version: str = "0.5.2"):
        self.data = {
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

    def to_dict(self):
        return self.data

    def add_nodes(
        self,
        nodeMappings: dict[str, NodeMapping]
        ):
        for _, nodeMapping in nodeMappings.items():
            self.add_node(nodeMapping)


    def add_node(
        self,
        nodeMapping: NodeMapping
        ):

        caption = nodeMapping.caption
        if caption is None:
            logging.error(f"Node {nodeMapping} does not have a caption")

        # Add to graph:nodes
        self.data["graph"]["nodes"].append({
            "id": nodeMapping.id,
            "position": nodeMapping.position,
            "caption": caption
        })

        # TODO: Add .csv file origin and reference info in dataModel:fileModel:fileSchemas
        self.data["dataModel"]["fileModel"]["fileSchemas"].update(file_schema_node(nodeMapping))

        # TODO: Add to graphModel:nodeSchemas

        # TODO: Examples of labelProperties

        # TODO: Add to graphModel:mappingModel:nodeMappings


    def add_relationships(
        self,
        relationshipMappings: dict[str, RelationshipMapping]
        ):
        for _, relationshipMapping in relationshipMappings.items():
            self.add_relationship(relationshipMapping)

    def add_relationship(
        self,
        relationship: RelationshipMapping
        ):
        # Add to graph:relationships
        self.data["graph"]["relationships"].append({
            "id": relationship.id,
            "type": relationship.type,
            "fromId": relationship.start_node_id,
            "toId": relationship.end_node_id
        })
        
        # TODO: Add to graphModel:relationshipSchemas
        self.data['dataModel']['graphModel']['relationshipSchemas'].update(
            {
                f"{relationship.id}":{
                    "type": relationship.type,
                    "sourceNodeSchema": relationship.start_node_id,
                    "targetNodeSchema": relationship.end_node_id,
                    "properties":[
                        graph_model_relationship_property(property) for property in relationship.properties
                    ]
                }
            }
        )