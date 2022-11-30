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


def graph_model_property(property: PropertyMapping)-> dict:
    result = {
        "property": property.name,
        "type": property.type.to_string().lower(),
        "identifier": property.id
        }
    return result

def mapping_model_node_mappings(node:NodeMapping)->list[dict[str,str]]:
    result = []
    for property in node.properties:
        result.append({
            "field": property.name,
        })
    return result

class DataImporterJson():
    def __init__(self, version: str = "0.7.0"):
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

        # dataModel:fileModel:fileSchemas
        self.data["dataModel"]["fileModel"]["fileSchemas"].update(file_schema_node(nodeMapping))

        # TODO: Add to graphModel:nodeSchemas
        # TODO: complete
        self.data["dataModel"]["graphModel"]["nodeSchemas"].update(
            {
                f"{nodeMapping.id}":{
                    "label": nodeMapping.caption,
                    "additionalLabels":nodeMapping.labels,
                    "labelProperties":[],
                    "properties":[
                        graph_model_property(property) for property in nodeMapping.properties
                    ],
                    "key":{
                        "properties":[nodeMapping.key_property.id],
                        "name":""
                    }
                }
            }
        )

        # TODO: Examples of labelProperties

        # Add to dataModel:mappingModel:nodeMappings
        self.data["dataModel"]["mappingModel"]["nodeMappings"].update(
            {
                f"{nodeMapping.id}":{
                    "fileSchema": nodeMapping.filename(),
                    "nodeSchema": nodeMapping.id,
                    "mappings":mapping_model_node_mappings(nodeMapping)
                }
            }
        )


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
        
        # Add to graphModel:relationshipSchemas
        self.data['dataModel']['graphModel']['relationshipSchemas'].update(
            {
                f"{relationship.id}":{
                    "type": relationship.type,
                    "sourceNodeSchema": relationship.start_node_id,
                    "targetNodeSchema": relationship.end_node_id,
                    "properties":[
                        graph_model_property(property) for property in relationship.properties
                    ]
                }
            }
        )

        # TODO: Add to grap hModel:mappingModel:nodeMappings
