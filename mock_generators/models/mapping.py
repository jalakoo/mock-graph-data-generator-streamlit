
from models.node_mapping import NodeMapping
import json
import logging
import sys


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

    def is_empty(self):
        if len(self.nodes) > 0:
            return False
        if len(self.relationships) > 0:
            return False
        return True

    def is_valid(self):
        # TODO: Actually validate data content

        for node in self.nodes.values():
            if node.ready_to_generate() == False:
                # logging.info(f'mapping.py (model): is_valid. Node not ready to generate: {node}')
                return False
        for relationship in self.relationships.values():
            if relationship.ready_to_generate() == False:
                # logging.info(f'mapping.py (model): is_valid. Relationship not ready to generate: {relationship}')
                return False

        try:
            json.loads(json.dumps(self.to_dict()))
            # logging.info(f'mapping.py (model): is_valid. SUCCESS for mapping: {self}')
            return True
        except ValueError as err:
            logging.error(f'mapping.py (model): is_valid. ERROR: {err} for mapping: {self}')
            return False
        except:
            logging.error(f'mapping.py (model): is_valid. ERROR: {sys.exc_info()[0]} for mapping: {self}')
            return False