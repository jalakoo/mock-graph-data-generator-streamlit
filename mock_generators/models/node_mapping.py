from models.property_mapping import PropertyMapping
from models.generator import Generator
import sys

class NodeMapping():

    def __init__(
        self, 
        id: str,
        position: dict,   # ie: {x: 0, y: 0}
        caption: str,
        labels: list[str], 
        properties: list[PropertyMapping], 
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
            "properties": [property.to_dict() for property in self.properties],
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
        #         "first_name": "John",
        #         "last_name": "Doe"
        #     },
        #     {
        #         "first_name": "Jane",
        #         "last_name": "Doe"
        #     }
        # ]
        count_generator = self.count_generator
        count_args = self.count_args
        count = None
        try:
            module = __import__(count_generator.import_url(), fromlist=['generate'])
            count = module.generate(count_args)
            result = []
            for _ in range(count):
                node_result = {}
                for property in self.properties:
                    args = property.args
                    value = property.generator.generate(args)
                    node_result[property.name] = value
                    result.append(node_result)
            self.generate_values = result
            return result
        except:
            raise Exception(f"Node mapping could not load count generator from url {count_generator.import_url()}, error: {str(sys.exc_info()[0])}")
