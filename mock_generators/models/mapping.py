
from models.generator import Generator, GeneratorType

class PropertyMapping():
    def __init__(
        self, 
        id: str,
        name: str, 
        type: GeneratorType, 
        generator: Generator, 
        generator_args: list[any]):
        self.id = id
        self.name = name
        self.type = type
        self.generator = generator
        self.generator_args = generator_args
        

class NodeMapping():
    def __init__(
        self, 
        id: str,
        labels: list[str], 
        properties: list[PropertyMapping], 
        count_generator: Generator):
        self.id = id
        self.labels = labels
        self.properties = properties
        self.generator = count_generator


class RelationshipMapping():
    def __init__(
        self, 
        id: str,
        type: str,
        start_node: NodeMapping, 
        end_node: NodeMapping, 
        properties: list[PropertyMapping], 
        count_generator: Generator):
        self.id = id
        self.type = type
        self.start_node = start_node
        self.end_node = end_node
        self.properties = properties
        self.generator = count_generator

class Mapping():
    # For storing mapping configurations
    def __init__(self, nodes = [NodeMapping], relationships = [RelationshipMapping]):
        self.nodes = nodes
        self.relationships = relationships