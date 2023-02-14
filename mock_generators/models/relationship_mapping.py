
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
import random
import sys
from copy import deepcopy
from list_utils import clean_list

class RelationshipMapping():

    @staticmethod
    def empty():
        return RelationshipMapping(
            rid = "",
            type = "",
            from_node = None,
            to_node = None,
            properties = {},
            count_generator = None,
            count_args = [],
            filter_generator = None,
            filter_args = [],
            assignment_generator = None,
            assignment_args = []
        )

    def __init__(
        self, 
        rid: str,
        type: str,
        properties: dict[str, PropertyMapping],
        from_node : NodeMapping,
        to_node : NodeMapping,
        # For determining count of relationships to generate
        count_generator: Generator,
        # For determining how to assign relationships -> to nodes
        assignment_generator: Generator,
        assignment_args: list[any] = [],
        count_args: list[any] = [],
        # TODO: Make below non-optional
        # For filtering from nodes
        filter_generator: Generator = None,
        filter_args: list[any] = [],

        ):
        self.rid = rid
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = clean_list(count_args)
        self.generated_values = None
        self.filter_generator = filter_generator
        self.filter_generator_args = clean_list(filter_args)
        self.assignment_generator = assignment_generator
        self.assignment_args = clean_list(assignment_args)

    def __str__(self):
        return f"RelationshipMapping(rid={self.rid}, type={self.type}, from_node={self.from_node}, to_node={self.to_node}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "rid": self.rid,
            "type": self.type,
            "from_node": self.from_node.to_dict() if self.from_node is not None else None,
            "to_node": self.to_node.to_dict() if self.to_node is not None else None,
            "properties": {key: property.to_dict() for (key,property) in self.properties.items()},
            "count_generator": self.count_generator.to_dict() if self.count_generator is not None else None,
            "count_args": self.count_args
            # TODO: Add filter_generator, filter_args, assignment_generator, assignment_args
        }

    def filename(self):
        from_node_name = self.from_node.caption.lower()
        to_node_name = self.to_node.caption.lower()
        return f"{from_node_name}_{self.type.lower()}_{to_node_name}_{self.rid.lower()}"

    # TODO: Verify unique keys are respected during generation

    def ready_to_generate(self):
        if self.type is None:
            return False
        if self.from_node is None:
            return False
        if self.to_node is None:
            return False
        if self.count_generator is None:
            return False
        return True

    def generate_values(
        self, 
        )-> list[dict]:


        # Make sure from and to nodes have generated values already
        if self.from_node.generated_values == None:
            self.from_node.generate_values()
        if self.to_node.generated_values == None:
            self.to_node.generate_values()

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

        # TODO: Run filter generator here to determine which source nodes to process

        # Make a copy of the generated list
        values = deepcopy(self.to_node.generated_values)

        # Iterate through every generated source node
        for value_dict in self.from_node.generated_values:
            # dict of property names and generated values

            # Decide on how many of these relationships to generate
            count = 0
            try:
                count = self.count_generator.generate(self.count_args)
            except:
                # Generator not found or other code error
                raise Exception(f"Relationship mapping could not generate a number of relationships to continue generation process, error: {str(sys.exc_info()[0])}")

            # Validate something to process for this source node
            if value_dict.keys() is None or len(value_dict.keys()) == 0:
                # Data importer requires at least one property-value
                raise Exception(f"No properties found for NodeMapping: {self.from_node}")

            # Get the key property name and value for the source node record
            from_node_key_property_name = self.from_node.key_property.name
            from_node_key_property_value = value_dict.get(from_node_key_property_name, None)
            if from_node_key_property_value is None:
                raise Exception(f"Key property '{from_node_key_property_name}' not found in node: {value_dict}")

            # If count is zero - no relationship to generate for the current source node

            # Generate a new relationship for each count
            for i in range(count):
                # Select a random target node

                if values is None or len(values) == 0:
                    # TODO: This appears to break the randomization
                    logging.info(f'relationship_mapping.py: values exhausted at index {i} before count of {count} reached. Values: {len(values)}')
                    continue

                # Extract results. Values will be passed back through the next iteration in case the generator returns a modified list

                # TODO: values does not change after this call
                to_node_value_dict, new_values = self.assignment_generator.generate(values)

                values = new_values

                # Types of randomization generators to consider:
                # - Pure Random
                # - Random with a bias towards nodes with fewer relationships
                # - Random with a bias towards nodes with more relationships
                # - Random Unique (no duplicates)
                # - Random Exhaustive (attempt to exhaust all nodes before repeating)

                # Get key property name and value for target record
                to_node_key_property_name = self.to_node.key_property.name
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

        # Store results for reference
        self.generated_values = all_results
        # logging.info(f'relationship_mapping.py: 1 value: {self.generated_values[0]}')
        return self.generated_values
        