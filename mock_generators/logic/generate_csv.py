from models.mapping import Mapping
import logging
import logging
from logic.generate_csv_nodes import export_csv_node
from logic.generate_csv_relationships import export_csv_relationship

def generate_csv(
    mapping: Mapping,
    export_folder: str) -> bool:
    # Returns True if files generated, False if not
        
    # Generate node values    
    for _, node in mapping.nodes.items():
        # Each nodeMapping is capable of generating and retaining it's own mock list data
        values : list[dict] = node.generate_values()
        if values is None or values == []:
            logging.warning(f'No values generated for node {node.caption}')
            return False

        export_csv_node(f'{node.filename()}.csv', values, export_folder)

    # Generate relationships, or more accurately, the csv files that
    # the data-importer will use to know which created nodes are connected with the mapped relationships
    for _, relationship in mapping.relationships.items():
        # Each node mapping is capable of generating and storing it's own list of mock list data, so the relationship mappings will use that data. Relationship mappings HOWEVER, do not store their own mock data as it isn't needed beyond this final export step.
        r_values : list[dict] = relationship.generate_values()
        export_csv_relationship(f'{relationship.filename()}.csv', r_values, export_folder)

    return True