# For converting data from various forms to other forms
from streamlit_agraph import agraph, Node, Edge, Config
import logging
import json

def random_coordinates_for(
        number: int):
    import numpy as np

    # Generate random coordinates
    min_range = 0
    max_width = number * 1000
    x_values = np.random.uniform(min_range, max_width, number)
    y_values = np.random.uniform(min_range, max_width, number)

    # Create list of (x, y) coordinates
    coordinates = list(zip(x_values, y_values))
    return coordinates


def agraph_data_from_response(response: str)->tuple[any, any, any]:
    # Returns agraph compatible nodes, edges, and config
    logging.debug(f'Response: {response}')
    # Response will be a list of 3 item tuples
    try:
        answers = json.loads(response)
    except Exception as e:
        logging.error(e)
        return None, None, None
    print(f'JSON: {answers}')
    if isinstance(answers, list) == False:
        logging.error(f'Response could not be converted to list, got {type(answers)} instead.')
        return None, None, None
    nodes = []
    # node_labels = []
    edges = []
    for idx, item in enumerate(answers):
        if item is None or len(item) != 3:
            continue
        n1_label = item[0]
        r = item[1]
        n2_label = item[2]

        # We only want to add agraph nodes with the same label once in our return

        # Gross but works
        add_n1 = True
        for node in nodes:
            if node.label == n1_label:
                add_n1 = False
        if add_n1:
            nodes.append(Node(id=n1_label, label=n1_label))

        add_n2 = True
        for node in nodes:
            if node.label == n2_label:
                add_n2 = False
        if add_n2:
            nodes.append(Node(id=n2_label, label=n2_label))

        # agraph requires source and target ids to use what we consider labels
        edge = Edge(source=n1_label, target=n2_label, label=r)
        edges.append(edge)
    config = Config(
        width=800, 
        height=800, 
        backgroundColor="#000000",
        directed=True)
    return (nodes, edges, config)


def convert_agraph_nodes_to_arrows_nodes(
        agraph_nodes: list
)-> list[dict]:
    # Convert agraph nodes to arrows nodes
    arrows_nodes = []

    # Generate random coordinates to init new arrows nodes with - since we can't extract the location data from agraph
    coordinates = random_coordinates_for(len(agraph_nodes))

    for nidx, node in enumerate(agraph_nodes):
        new_node = convert_agraph_node_to_arrows_node(
            nidx, node, coordinates[nidx][0], coordinates[nidx][1])
        arrows_nodes.append(new_node)
    return arrows_nodes

def convert_agraph_node_to_arrows_node(
        idx, 
        node,
        x,
        y):
    # Convert agraph node to arrows node
    arrows_node = {
        "id": f'n{idx+1}',
        "caption": node.label,
        "position": {
            "x": x,
            "y": y,
        },
        "labels":[],
        "style": {},
        "properties": {}
    }
    return arrows_node

def convert_agraph_edge_to_arrows_relationship(
        idx, 
        edge, 
        arrows_nodes: list):
    # Example: {'source': 'People', 'from': 'People', 'to': 'Cars', 'color': '#F7A7A6', 'label': 'DRIVE'}
    source_node_label = edge.source
    target_node_label = edge.to
    source_node_id = None
    target_node_id = None

    for node in arrows_nodes:
        if node['caption'] == source_node_label:
            source_node_id = node['id']
        if node['caption'] == target_node_label:
            target_node_id = node['id']

    if source_node_id is None or target_node_id is None:
        node_info = [node.__dict__ for node in arrows_nodes]
        logging.error(f'Could not find source or target node for edge {edge.__dict__} from nodes: {node_info}')
        return None
    edge_type = edge.label
    arrows_relationship = {
        "id": f'n{idx+1}',
        "fromId": source_node_id,
        "toId": target_node_id,
        "type": edge_type,
        "properties": {},
        "style": {}
    }
    return arrows_relationship

def convert_agraph_to_arrows(agraph_nodes, agraph_edges):
    arrows_nodes = convert_agraph_nodes_to_arrows_nodes(agraph_nodes)

    arrows_relationships = []
    for eidx, edge in enumerate(agraph_edges):
        new_relationship = convert_agraph_edge_to_arrows_relationship(eidx, edge, arrows_nodes=arrows_nodes)
        arrows_relationships.append(new_relationship)
    arrows_json = {
        "nodes": arrows_nodes,
        "relationships": arrows_relationships,
          "style": {
            "font-family": "sans-serif",
            "background-color": "#ffffff",
            "background-image": "",
            "background-size": "100%",
            "node-color": "#ffffff",
            "border-width": 4,
            "border-color": "#000000",
            "radius": 50,
            "node-padding": 5,
            "node-margin": 2,
            "outside-position": "auto",
            "node-icon-image": "",
            "node-background-image": "",
            "icon-position": "inside",
            "icon-size": 64,
            "caption-position": "inside",
            "caption-max-width": 200,
            "caption-color": "#000000",
            "caption-font-size": 50,
            "caption-font-weight": "normal",
            "label-position": "inside",
            "label-display": "pill",
            "label-color": "#000000",
            "label-background-color": "#ffffff",
            "label-border-color": "#000000",
            "label-border-width": 4,
            "label-font-size": 40,
            "label-padding": 5,
            "label-margin": 4,
            "directionality": "directed",
            "detail-position": "inline",
            "detail-orientation": "parallel",
            "arrow-width": 5,
            "arrow-color": "#000000",
            "margin-start": 5,
            "margin-end": 5,
            "margin-peer": 20,
            "attachment-start": "normal",
            "attachment-end": "normal",
            "relationship-icon-image": "",
            "type-color": "#000000",
            "type-background-color": "#ffffff",
            "type-border-color": "#000000",
            "type-border-width": 0,
            "type-font-size": 16,
            "type-padding": 5,
            "property-position": "outside",
            "property-alignment": "colon",
            "property-color": "#000000",
            "property-font-size": 16,
            "property-font-weight": "normal"
        }
    }
    return arrows_json
    