
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
import random

class RelationshipMapping():

    def __init__(
        self, 
        id: str,
        type: str,
        from_node : NodeMapping,
        to_node : NodeMapping,
        properties: dict[str, PropertyMapping],
        count_generator: Generator,
        count_args: list[any] = []
        ):
        self.id = id
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = count_args
        self.generated_values = None

    def __str__(self):
        return f"RelationshipMapping(id={self.id}, type={self.type}, from_node={self.from_node.to_dict()}, to_node={self.to_node.to_dict()}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "from_node": self.from_node.to_dict(),
            "to_node": self.to_node.to_dict(),
            "properties": {key: property.to_dict() for (key,property) in self.properties.items()},
            "count_generator": self.count_generator.to_dict(),
            "count_args": self.count_args
        }

    def filename(self):
        from_node_name = self.from_node.caption.lower()
        to_node_name = self.to_node.caption.lower()
        return f"{from_node_name}_{self.type.lower()}_{to_node_name}_{self.id.lower()}"

    # TODO: Verify unique keys are respected during generation

    def generate_values(
        self, 
        # all_node_values: dict[NodeMapping, list[dict]]
        )-> list[dict]:

        # Sample incoming all_node_values:
        # {
        #   "<node_mapping>":[
        #       {
        #       "first_name":"John",
        #       "last_name":"Doe"
        #      }  
        #   ]
        # }

        if self.from_node == None:
            raise Exception(f"RelationshipMapping {self} not assigned a from_node before generating values")
        if self.to_node == None:
            raise Exception(f"RelationshipMapping {self} not assigned a to_node before generating values")

        from_node = self.from_node
        to_node = self.to_node

        # Make sure from and to nodes have generated values already
        if from_node.generated_values == None:
            from_node.generate_values()
        if to_node.generated_values == None:
            to_node.generate_values()

        # Sample return list:
        # [
        #  {
        #    "<from_node_key_property_name>": "n1_abc",
        #    "<to_node_key_property_name>": "n2_abc",
        #    "since": "2020-01-01"
        #   }
        # ]


        # Store generated relationships to return
        all_results = []

        # Iterate through every generated source node
        for value_dict in from_node.generated_values:
            # value_dict = dict of property names and generated values

            # Validate we have anything to process
            if value_dict.keys() is None or len(value_dict.keys()) == 0:
                raise Exception(f"No properties found for NodeMapping: {from_node}")

            # Get the key property name and value for source node
            from_node_key_property_name = from_node.key_property.name
            from_node_key_property_value = value_dict[from_node_key_property_name]


            # Select a random target node
            to_node_value_dict = random.choice(to_node.generated_values)

            # Get key property name and value for target record
            to_node_key_property_name = to_node.key_property.name
            to_node_key_property_value = to_node_value_dict[to_node_key_property_name]

            # Generate the relationship
            result = {
                f'_from_{from_node_key_property_name}': from_node_key_property_value,
                f'_to_{to_node_key_property_name}': to_node_key_property_value
            }

            # Generate the properties
            for property_name, property_mapping in self.properties.items():
                result[property_name] = property_mapping.generate_value()

            all_results.append(result)

        logging.info(f'Generated {len(all_results)} records for relationship type: {self.type}')
        self.generated_values = all_results
        return self.generated_values
        