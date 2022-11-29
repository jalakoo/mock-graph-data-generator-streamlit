
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator

class RelationshipMapping():

    @staticmethod
    def empty():
        return RelationshipMapping(
            id = None,
            type = None,
            start_node = NodeMapping.empty(),
            end_node = NodeMapping.empty(),
            properties = [],
            count_generator = None,
            count_generator_args = []
        )

    def __init__(
        self, 
        id: str,
        type: str,
        start_node: NodeMapping, 
        end_node: NodeMapping, 
        properties: list[PropertyMapping], 
        count_generator: Generator,
        count_generator_args: list[any] = []
        ):
        self.id = id
        self.type = type
        self.start_node = start_node
        self.end_node = end_node
        self.properties = properties
        self.count_generator = count_generator
        self.count_generator_args = count_generator_args

    def __str__(self):
        return f"RelationshipMapping(id={self.id}, type={self.type}, start_node={self.start_node}, end_node={self.end_node}, properties={self.properties}, count_generator={self.count_generator}, count_generator_args={self.count_generator_args})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "start_node": self.start_node.to_dict(),
            "end_node": self.end_node.to_dict(),
            "properties": [property.to_dict() for property in self.properties],
            "count_generator": self.count_generator.to_dict(),
            "count_generator_args": self.count_generator_args
        }

    def filename(self):
        return f"{self.type}_{self.id}"