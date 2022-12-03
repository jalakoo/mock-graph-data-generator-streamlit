from models.property_mapping import PropertyMapping
from models.generator import Generator
import sys
import uuid
import logging

class NodeMapping():

    def __init__(
        self, 
        id: str,
        position: dict,   # ie: {x: 0, y: 0}
        caption: str,
        labels: list[str], 
        properties: dict[str, PropertyMapping],
        # properties: list[PropertyMapping], 
        count_generator: Generator,
        count_args: list[any] = [],
        key_property: PropertyMapping = None):
        self.id = id
        self.position = position
        self.caption = caption
        self.labels = labels
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = count_args
        self.key_property = key_property # Property to use as unique key for this node

    def __str__(self):
        return f"NodeMapping(id={self.id}, caption={self.caption}, labels={self.labels}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args}, key_property={self.key_property})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "position": self.position,
            "labels": self.labels,
            "properties": {key: property.to_dict() for (key, property) in self.properties.items()},
            "count_generator": self.count_generator.to_dict(),
            "count_args": self.count_args,
            "key_property" : self.key_property.to_dict()
        }

    def filename(self):
        return f"{self.caption.lower()}_{self.id.lower()}"

    def generate_values(self) -> list[dict]:
        # returns a list of dicts with the generated values
        # Example return:
        # [
        #     {
        #         "_uid": "n1_abc",
        #         "first_name": "John",
        #         "last_name": "Doe"
        #     },
        #     {
        #         "_uid": "n1_xyz",
        #         "first_name": "Jane",
        #         "last_name": "Doe"
        #     }
        # ]
        count = 0
        result = []
        try:
            count = self.count_generator.generate(self.count_args)
        except:
            raise Exception(f"Node mapping could not generate a number of nodes to continue generation process, error: {str(sys.exc_info()[0])}")
        # finally:
        #     logging.info(f'Generated {count} node values for node  {self.caption}')

        try:
            for _ in range(count):
                node_result = {}
                # TODO: change to:
                for property_name, property in self.properties.items():
                # for property in self.properties:
                    value = property.generate_value()
                    node_result[property_name] = value
                    result.append(node_result)
                node_result["_uid"] = f"{self.id}_{str(uuid.uuid4())[:8]}"
                self.generate_values = result
        except:
            raise Exception(f"Node mapping could not generate property values, error: {str(sys.exc_info()[0])}")

        logging.info(f'Generated {len(result)} node records for node  {self.caption}')
        self.generate_values = result
        return self.generate_values