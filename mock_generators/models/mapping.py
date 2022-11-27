
from models.generator import Generator, GeneratorType

class PropertyMapping():

    @staticmethod
    def empty():
        return PropertyMapping(
            id = "",
            name = "",
            type = "",
            generator = None,
            generator_args = {}
        )

    def __init__(
        self, 
        id: str,
        name: str = None, 
        type: GeneratorType = None, 
        generator: Generator = None, 
        generator_args: list[any] = []):
        self.id = id
        self.name = name
        self.type = type
        self.generator = generator
        self.generator_args = generator_args

    def __str__(self):
        return f"PropertyMapping(id={self.id}, name={self.name}, type={self.type}, generator={self.generator}, generator_args={self.generator_args})"
        
    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "generator": self.generator.to_dict(),
            "generator_args": self.generator_args
        }



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
            count_generator_args = []
        )

    def __init__(
        self, 
        id: str,
        position: dict,
        caption: str,
        labels: list[str], 
        properties: list[PropertyMapping], 
        count_generator: Generator,
        count_generator_args: list[any] = []):
        self.id = id
        self.position = position
        self.caption = caption
        self.labels = labels
        self.properties = properties
        self.count_generator = count_generator
        self.count_generator_args = count_generator_args

    def __str__(self):
        return f"NodeMapping(id={self.id}, caption={self.caption}, labels={self.labels}, properties={self.properties}, count_generator={self.count_generator}, count_generator_args={self.count_generator_args})"

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
            "count_generator_args": self.count_generator_args
        }

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

class Mapping():
    # For storing mapping configurations
    def __init__(self, nodes : dict = {}, relationships : dict = {}):
        self.nodes = nodes
        self.relationships = relationships

    def __str__(self):
        return f"'Mapping':{{'nodes': {self.nodes}, 'relationships': {self.relationships} }})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "mapping" :{
                "nodes": {key: value.to_dict() for key, value in self.nodes.items()},
                "relationships": {key: value.to_dict() for key, value in self.relationships.items()}
            }
        }