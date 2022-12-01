
# from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import sys

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
        self.generated_values = []

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

    def generate_values(self)-> list[dict]:
        count_generator = self.count_generator
        count_args = self.count_args
        count = None
        try:
            module = __import__(count_generator.import_url(), fromlist=['generate'])
            count = module.generate(count_args)
            result = []
            for _ in range(count):
                relationship_result = {}
                # TODO: Get actual node values

                # TODO: Generate relationship values

                # Generate relationship properties
                for property in self.properties:
                    args = property.args
                    value = property.generator.generate(args)
                    relationship_result[property.name] = value
                    result.append(relationship_result)
            self.generate_values = result
            return result
        except:
            raise Exception(f"Node mapping could not load count generator from url {count_generator.import_url()}, error: {str(sys.exc_info()[0])}")