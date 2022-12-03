
# from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import sys
import uuid
import logging

class RelationshipMapping():

    def __init__(
        self, 
        id: str,
        type: str,
        start_node_id: str, 
        end_node_id: str, 
        properties: dict[str, PropertyMapping],
        count_generator: Generator,
        count_args: list[any] = []
        ):
        self.id = id
        self.type = type
        self.start_node_id = start_node_id
        self.end_node_id = end_node_id
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = count_args
        self.generated_values = []

    def __str__(self):
        return f"RelationshipMapping(id={self.id}, type={self.type}, start_node_id={self.start_node_id}, end_node_id={self.end_node_id}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "start_node_id": self.start_node_id,
            "end_node_id": self.end_node_id,
            "properties": [property.to_dict() for property in self.properties.items()],
            "count_generator": self.count_generator.to_dict(),
            "count_args": self.count_args
        }

    def filename(self):
        return f"{self.type.lower()}_{self.id.lower()}"

    def generate_values(
        self, 
        all_node_values: dict[list[dict]]
        )-> list[dict]:

        # Sample incoming all_node_values:
        # {
        #   "<node_mapping_id>":[
        #       {
        #       "first_name":"John",
        #       "last_name":"Doe"
        #      }  
        #   ]
        # }
        #  This dict keys should include the node ids found in this relationship's fromId and toId properties
        if self.start_node_id not in all_node_values:
            raise Exception(f"NodeMapping with id {self.start_node_id} not found in all_node_values")
        if self.end_node_id not in all_node_values:
            raise Exception(f"NodeMapping with id {self.end_node_id} not found in all_node_values")

        # Sample exported list:
        # [
        #  {
        #    "_uid": "n1_abc",
        #    "since": "2020-01-01"
        #   }
        # ]


        # Generate number of relationships to create
        count = None
        try:
            count = self.count_generator.generate(self.count_args)
        except:
            raise Exception(f"Relationship mapping could not generate a count for producing values. Mapping: {self}\n\nError: {str(sys.exc_info()[0])}")

        # Generate relationships
        if all_node_values is None or len(all_node_values.keys()) == 0:
            raise Exception("No node values provided to relationship mapping generator")
        result = []
        for node_id, all_node_values in all_node_values.keys():
            try:
                for i in range(count):
                    # Generate each relationship with any optional properties
                    relationship_result = {}

                    # TODO: Update to use dict properties like nodes
                    # Generate new relationship properties
                    for property_name, property in self.properties.items():
                    # for property in self.properties:
                        value = property.generate_value()
                        relationship_result[property_name] = value
                        result.append(relationship_result)

                    # Add source node
                    relationship_result['_from_node_id'] = self.start_node_id

                    # Add target node
                    relationship_result['_to_node_id'] = self.end_node_id

                    # Add unique id to this relationship entry
                    relationship_result["_uid"] = f"{self.id}_{str(uuid.uuid4())[:8]}"

                    result.append(relationship_result)
            except:
                raise Exception(f"Relationship mapping for {self.type} could not generate values for node id: {node_id}\n\nError: {str(sys.exc_info()[0])}")
        
        logging.info(f'Generated {len(result)} records for relationship type: {self.type}')
        self.generated_values = result
        return self.generated_values
        