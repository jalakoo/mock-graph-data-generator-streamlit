from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
import logging
from models.generator import GeneratorType
import datetime

def file_schema_for_property(property: PropertyMapping)-> dict:

    sample_value = property.generator.generate(property.args)

    # Why is it so tough to catch datetime objects?
    if isinstance(sample_value, datetime.date):
        sample_value = sample_value.isoformat()
    if type(sample_value) is datetime:
        sample_value = sample_value.isoformat()
    if property.type == GeneratorType.DATETIME:
        sample_value = sample_value.isoformat()

    result = {
        "name": property.name,
        "type": property.type.to_string().lower(),
        "sample": sample_value,
        "include": True
    }
    return result

def file_schema_for_relationship(relationship: RelationshipMapping)-> list[dict]:
    # A little different than nodes because we need to add the relationship properties and the from and to node information
    result = []
    for property in relationship.properties.values():
        result.append(file_schema_for_property(property))


    from_dict = file_schema_for_property(relationship.from_node.key_property)
    # prefixing property names in case the node key names are the same. Not strictly necessary but difficult to manually follow otherwise
    from_dict['name'] = f'_from_{from_dict["name"]}'
    result.append(from_dict)

    to_dict = file_schema_for_property(relationship.to_node.key_property)
    to_dict['name'] = f'_to_{to_dict["name"]}'
    result.append(to_dict)
    return result


def graph_model_property(property: PropertyMapping)-> dict:
    result = {
        "property": property.name,
        "type": property.type.to_string().lower(),
        "identifier": property.pid
        }
    return result

def mapping_model_node_mappings(node:NodeMapping)->list[dict[str,str]]:
    result = []
    for property in node.properties.values():
        result.append({
            "field": property.name,
        })
    return result

class DataImporterJson():
    # Object for converting mapping info to a JSON file that can be imported into the Data Importer

    # TODO: Use constants to define the keys for the JSON file

    def __init__(self, version: str = "0.7.1"):
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
        # TODO: Verify format is correct
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
            "id": nodeMapping.nid,
            "position": nodeMapping.position,
            "caption": caption
        })

        # dataModel:fileModel:fileSchemas
        try:
            self.data["dataModel"]["fileModel"]["fileSchemas"].update(
                {
                    f"{nodeMapping.filename()}.csv":{
                        "expanded": True,
                        "fields":[
                            file_schema_for_property(property) for property in nodeMapping.properties.values()
                        ]
                    }
                }
            )
        except:
            raise Exception(f'Error adding node {nodeMapping} to fileSchemas')

        # Add to dataModel:graphModel:nodeSchemas
        try: 
            self.data["dataModel"]["graphModel"]["nodeSchemas"].update(
                {
                    f"{nodeMapping.nid}":{
                        "label": nodeMapping.caption,
                        "additionLabels":nodeMapping.labels,
                        "labelProperties":[],
                        "properties":[
                            graph_model_property(property) for property in nodeMapping.properties.values()
                        ],
                        "key":{
                            "properties":[nodeMapping.key_property.pid],
                            "name":""
                        }
                    }
                }
            )
        except:
            raise Exception(f'Error adding node {nodeMapping} to dataModel:graphModel:nodeSchemas')

        # TODO: Get Examples of labelProperties - are these even used by data importer?

        # Add to dataModel:mappingModel:nodeMappings
        try:
            self.data["dataModel"]["mappingModel"]["nodeMappings"].update(
                {
                    f"{nodeMapping.nid}":{
                        "fileSchema": f'{nodeMapping.filename()}.csv',
                        "nodeSchema": nodeMapping.nid,
                        "mappings":mapping_model_node_mappings(nodeMapping)
                    }
                }
            )
        except:
            raise Exception(f'Error adding node {nodeMapping} to dataModel:mappingModel:nodeMappings')

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

        # In case relationshipMapping has not yet generated data
        if relationship.generated_values is None:
            relationship.generate_values()

        # Add to graph:relationships
        try: 
            self.data["graph"]["relationships"].append({
                "id": relationship.rid,
                "type": relationship.type,
                "fromId": relationship.from_node.nid,
                "toId": relationship.to_node.nid
            })
        except:
            raise Exception(f'Error adding relationship {relationship} to graph:relationships')

        # Add to dataModel:graphModel:relationshipSchemas
        # EXAMPLE
        # "n2": {
        #   "type": "CREATED",
        #   "sourceNodeSchema": "n0",
        #   "targetNodeSchema": "n3",
        #   "properties": [
        #     {
        #       "property": "created_at",
        #       "type": "datetime",
        #       "identifier": "Qd0FzMHkcCxGIzSnBqbhb"
        #     }
        #   ]
        # }
        try:
            self.data['dataModel']['graphModel']['relationshipSchemas'].update(
                {
                    f"{relationship.rid}":{
                        "type": relationship.type,
                        "sourceNodeSchema": relationship.from_node.nid,
                        "targetNodeSchema": relationship.to_node.nid,
                        "properties":[
                            graph_model_property(property) for property in relationship.properties.values()
                        ]
                    }
                }
            )
        except:
            raise Exception(f'Error adding relationship {relationship} to dataModel:graphModel:relationshipSchemas')

        # Add dataModel:fileModel:fileSchemas
        # Get filename of csv generated for relationships
        #  EXAMPLE
        # "works_at.csv": {
        #   "expanded": true,
        #   "fields": [
        #     {
        #       "name": "from_node_id",
        #       "type": "string",
        #       "sample": "cdab7d16-1147-4de4-8eb9-b9d3a541a617",
        #       "include": true
        #     },
        #     {
        #       "name": "to_node_id",
        #       "type": "string",
        #       "sample": "4e228111-d659-47e5-a560-d46a81ed3927",
        #       "include": true
        #     }
        #   ]
        # }
        try:
            self.data['dataModel']['fileModel']['fileSchemas'].update(
                {
                    f'{relationship.filename()}.csv':{
                        "expanded": True,
                        "fields": file_schema_for_relationship(relationship)
                    }
                }
            )
        except:
            raise Exception(f'Error adding relationship {relationship} to dataModel:fileModel:fileSchemas')

        # Add to dataModel:graphModel:mappingModel:relationshipMappings
        # EXAMPLE
        # "n0": {
        #   "relationshipSchema": "n0",
        #   "mappings": [],
        #   "sourceMappings": [
        #     {
        #       "field": "company_id"
        #     }
        #   ],
        #   "targetMappings": [
        #     {
        #       "field": "company_id"
        #     }
        #   ],
        #   "fileSchema": "people.csv"
        # },

        try:
            self.data['dataModel']['mappingModel']['relationshipMappings'].update(
            {
                    f"{relationship.rid}":{
                        "relationshipSchema": f'{relationship.rid}',
                        "mappings":[],
                        # NOTE: The prefixing
                        "sourceMappings": [{
                            "field":f"_from_{relationship.from_node.key_property.name}"
                        }],
                        "targetMappings": [{
                            "field":f"_to_{relationship.to_node.key_property.name}"
                        }],
                        "fileSchema": f'{relationship.filename()}.csv', 
                    }
                }
            )
        except:
            raise Exception(f'Error adding relationship {relationship} to dataModel:graphModel:mappingModel:relationshipMappings')