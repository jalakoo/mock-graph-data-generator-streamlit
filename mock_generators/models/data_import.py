from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
import logging


def file_schema_node_property(property: PropertyMapping)-> dict:
    sample_value = property.generator.run(property.args)
    result = {
        "name": property.name,
        "type": property.type.to_string(),
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
        relationshipMappings: list[RelationshipMapping]
        ):
        for relationshipMapping in relationshipMappings:
            self.add_relationship(relationshipMapping)

    def add_relationship(
        self,
        relationshipMapping: RelationshipMapping
        ):
        # Add to graph:relationships
        # self.data["graph"]["relationships"].append({
        #     "id": relationshipMapping.id,
        #     "type": relationshipMapping.type,
        #     "fromId": relationshipMapping.fromId,
        #     "toId": relationshipMapping.toId
        # })
        print('add_relationship tbd')