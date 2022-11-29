from models.property_mapping import PropertyMapping
from models.generator import Generator

class NodeMapping():

    @staticmethod
    def empty():
        return NodeMapping(
            id = None,
            position = {"x": 0, "y": 0},
            caption = "",
            labels = [],
            properties = [],
            count_generator = None,
            count_args = [],
            key_property = None
        )

    def __init__(
        self, 
        id: str,
        position: dict,
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
        return f"{self.caption}_{self.id}"