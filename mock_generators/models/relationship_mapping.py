
# from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator

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