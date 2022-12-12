
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
import random
import sys

class RelationshipMapping():

    def __init__(
        self, 
        id: str,
        type: str,
        properties: dict[str, PropertyMapping],
        from_node : NodeMapping = None,
        to_node : NodeMapping = None,
        count_generator: Generator = None,
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

            # Decide on how many of these relationships to generate
            count = 0
            try:
                count = self.count_generator.generate(self.count_args)
            except:
                raise Exception(f"Relationship mapping could not generate a number of relationships to continue generation process, error: {str(sys.exc_info()[0])}")

            # Validate we have anything to process for this source node
            if value_dict.keys() is None or len(value_dict.keys()) == 0:
                raise Exception(f"No properties found for NodeMapping: {from_node}")

            # Get the key property name and value for source node
            from_node_key_property_name = from_node.key_property.name
            from_node_key_property_value = value_dict[from_node_key_property_name]

            # If count is zero - no relationship generated for the curent source node
            for _ in range(count):
                # Select a random target node
                # TODO: Implement variable randomization modes here
                to_node_value_dict = random.choice(to_node.generated_values)

                # Types of randomizations likely needed:
                # - Pure Random
                # - Random with a bias towards nodes with fewer relationships
                # - Random with a bias towards nodes with more relationships
                # - Random Unique (no duplicates)
                # - Random Exhaustive (attempt to exhaust all nodes before repeating)

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

                # Add the relationship to the list
                all_results.append(result)

        self.generated_values = all_results
        return self.generated_values
        