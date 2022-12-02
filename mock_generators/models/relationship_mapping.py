
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
        properties: list[PropertyMapping], 
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
            "properties": [property.to_dict() for property in self.properties],
            "count_generator": self.count_generator.to_dict(),
            "count_args": self.count_args
        }

    def filename(self):
        return f"{self.type.lower()}_{self.id.lower()}"

    def generate_values(
        self, 
        node_values: dict[list[dict]]
        )-> list[dict]:

        logging.info(f'relationship {self} received generate_values: number of node_values: {len(node_values)}')

        # Sample incoming node_values:
        # node_values: {
        #   "<node_id>":[
        #       {
        #       "first_name":"John",
        #       "last_name":"Doe"
        #      }  
        #   ]
        # }

        # Sample exported list:
        # [
        #  {
        #    "_uid": "n1_abc",
        #    "_type": "WORKS_AT",
        #    "since": "2020-01-01"
        #   }
        # ]

        # Get the generator used to generate the number of relationships
        # count_generator = self.count_generator
        # count_args = self.count_args
        # count = None

        # Get generated mock values for all nodes
        # from_node_values: dict[list[dict]] = node_values[self.start_node_id]
        for key, value in node_values.items():
            try:
                # Generate number of relationships for each node value
                # import_url = f"{count_generator.import_url()}"
                # module = __import__(import_url, fromlist=['generate'])
                # count = module.generate(count_args)
                count = self.count_generator.generate(self.count_args)
                result = []
                for i in range(count):
                    # Generate each relationship with any optional properties
                    relationship_result = {}

                    # Generate relationship properties
                    for property in self.properties:
                        value = property.generate_value()
                        relationship_result[property.name] = value
                        result.append(relationship_result)
                    
                    # Generate default info uid
                    # relationship_result['_uid'] = f"{self.id}_{i}"
                    # relationship_result['_type'] = self.type

                    # Get key property of source node
                    from_node_key_property = self.get_key_property(node_values[self.start_node_id])
                    sample_from = from_node_key_property.generate_value()
                    relationship_result['_from_node_key_sample'] = f"{sample_from}"
                    relationship_result['_from_node_key'] = from_node_key_property.name

                    # Get key property of target node
                    to_node_key_property = self.get_key_property(node_values[self.end_node_id])
                    sample_to = to_node_key_property.generate_value()
                    relationship_result['_to_node_key_sample'] = f"{sample_to}"
                    relationship_result['_to_node_key'] = to_node_key_property.name


                self.generated_values.append(result)
                return self.generated_values
            except:
                raise Exception(f"Relationship mapping could not load count generator from url {self.count_generator.import_url()}, error: {str(sys.exc_info()[0])}")