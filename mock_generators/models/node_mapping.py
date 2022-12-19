from models.property_mapping import PropertyMapping
from models.generator import Generator
import sys
import logging
from list_utils import clean_list

# TODO: Should have made these dataclasses
class NodeMapping():

    @staticmethod
    def empty():
        return NodeMapping(
            nid = "",
            position = {"x": 0, "y": 0},
            caption = "",
            labels = [],
            properties = {},
            count_generator = None,
            count_args = [],
            key_property = None
        )

    def __init__(
        self, 
        nid: str,
        position: dict,   # ie: {x: 0, y: 0}
        caption: str,
        labels: list[str], 
        properties: dict[str, PropertyMapping],
        count_generator: Generator,
        count_args: list[any],
        key_property: PropertyMapping):
        self.nid = nid
        self.position = position
        self.caption = caption
        self.labels = labels
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = count_args
        self.key_property = key_property # Property to use as unique key for this node
        self.generated_values = None # Will be a list[dict] when generated

    def __str__(self):
        return f"NodeMapping(nid={self.nid}, caption={self.caption}, labels={self.labels}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args}, key_property={self.key_property})"

    def __repr__(self):
        return self.__str__()


    def to_dict(self):
            return {
                "nid": self.nid,
                "caption": self.caption,
                "position": self.position,
                "labels": self.labels,
                "properties": {key: property.to_dict() for (key, property) in self.properties.items() if property.type is not None},
                "count_generator": self.count_generator.to_dict() if self.count_generator is not None else None,
                "count_args": clean_list(self.count_args),
                "key_property" : self.key_property.to_dict() if self.key_property is not None else None
            }

    def filename(self):
        return f"{self.caption.lower()}_{self.nid.lower()}"

    # TODO: Verify unique keys are respected during generation

    def ready_to_generate(self):
        if self.caption is None:
            return False
        if self.count_generator is None:
            return False
        if self.key_property is None:
            return False
        return True

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
        all_results = []
        try:
            count = self.count_generator.generate(self.count_args)
        except:
            raise Exception(f"Node mapping could not generate a number of nodes to continue generation process, error: {str(sys.exc_info()[0])}")

        try:
            for _ in range(count):
                node_result = {}
                for property_name, property in self.properties.items():
                    value = property.generate_value()
                    node_result[property_name] = value
                # node_result["_uid"] = f"{self.id}_{str(uuid.uuid4())[:8]}"
                all_results.append(node_result)
        except:
            raise Exception(f"Node mapping could not generate property values, error: {str(sys.exc_info()[0])}")
        
        # Store and return all_results
        self.generated_values = all_results
        logging.info(f'node_mapping.py: NodeMapping.generate_values() generated {len(self.generated_values)} values for node mapping {self.caption}')
        return self.generated_values