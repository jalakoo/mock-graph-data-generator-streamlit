
from models.node_mapping import NodeMapping

class Mapping():
    # For storing mapping configurations

    @staticmethod
    def empty():
        return Mapping({}, {})
        
    def __init__(self, nodes : dict[str, NodeMapping] = {}, relationships : dict = {}):
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