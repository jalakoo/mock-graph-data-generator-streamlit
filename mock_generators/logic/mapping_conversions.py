# For converting data from various forms to other forms
from streamlit_agraph import agraph, Node, Edge, Config

def convert_agraph_node_to_arrows_node(node):
    # Convert agraph node to arrows node
    # TODO: How do we handle position
    arrows_node = {
        "id": node.id,
        "caption": node.label,
        "position": {
            "x": 0,
            "y": 0,
        },
        "labels":[],
        "style": {},
        "properties": {}
    }
    return arrows_node

def convert_agraph_edge_to_arrows_relationship(edge):
    arrows_relationship = {
        "id": edge.id,
        "from": edge.source,
        "to": edge.target,
        "type": edge.label,
        "properties": {},
        "style": {}
    }
    return arrows_relationship

def convert_agraph_to_arrows_json(agraph_nodes, agraph_edges):
    # Convert agraph to arrows json
    arrows_nodes = [],
    arrows_relationships = []
    for node in agraph_nodes:
        new_node = convert_agraph_node_to_arrows_node(node)
        arrows_nodes.append(new_node)
    for edge in agraph_edges:
        new_relationship = convert_agraph_edge_to_arrows_relationship(edge)
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
    