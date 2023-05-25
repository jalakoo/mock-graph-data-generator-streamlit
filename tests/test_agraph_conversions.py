import pytest
from mock_generators.logic.agraph_conversions import convert_agraph_to_arrows, agraph_data_from_response, convert_agraph_nodes_to_arrows_nodes,convert_agraph_node_to_arrows_node, convert_agraph_edge_to_arrows_relationship,random_coordinates_for

from streamlit_agraph import agraph, Node, Edge, Config

class TestAgraphConversions:

    def test_agrph_data_from_response(self):
        response = """[
    [
        "Alice",
        "ROOMMATE",
        "Bob"
    ],
    [
        "Bob",
        "FRIEND_OF",
        "Charlie"
    ]
    ]
    """
        nodes, edges, config = agraph_data_from_response(response)
        print(f'{[node.__dict__ for node in nodes]}')
        assert len(nodes) == 3, f'Expected 3 nodes, got {len(nodes)}: nodes: {[node.__dict__ for node in nodes]}'
        assert len(edges) == 2, f'Expected 2 edges, got {len(edges)}: edges: {edges}'

        print(f'config: {config.__dict__}')
        assert config.width == "800px", f'Expected default config, got {config.__dict__}'
        assert config.height == "800px", f'Expected default config, got {config.__dict__}'
        assert config.backgroundColor == "#000000", f'Expected default config, got {config.__dict__}'

    def test_convert_agraph_edge_to_arrows_relationship(self):
        nodes = set()
        nodes.add(Node(id="n1", label="Alice"))
        nodes.add(Node(id="n2", label="Bob"))
        edge = Edge(source="Alice", target="Bob", label="FRIEND_OF")

        print(f'nodes: {[node.__dict__ for node in nodes]}')
        print(f'edge: {edge.__dict__}')

        arrows_nodes = convert_agraph_nodes_to_arrows_nodes(nodes)
        arrows_edge = convert_agraph_edge_to_arrows_relationship(0, edge, arrows_nodes)

        # NOTE: The edge may reverse the from and to ids
        print(f'arrows edge: {arrows_edge}')
        assert arrows_edge == {
            "id": "n1",
            "type": "FRIEND_OF",
            "fromId": "n1",
            "toId": "n2",
            "properties": {},
            "style": {}
        } or {
            "id": "n1",
            "type": "FRIEND_OF",
            "fromId": "n2",
            "toId": "n1",
            "properties": {},
            "style": {}
        }

    def test_convert_agraph_node_to_arrows_node(self):
        node = (Node(id="n1", label="Alice"))
        print(f'agraph_node: {node.__dict__}')
        coordinates = random_coordinates_for(1)
        arrows_node = convert_agraph_node_to_arrows_node(0, node, coordinates[0][0], coordinates[0][1])
        print(f'arrows_node: {arrows_node}')
        assert arrows_node == {
            "id": "n1",
            "caption": "Alice",
            "position": {
                "x": coordinates[0][0],
                "y": coordinates[0][1],
            },
            "labels": [],
            "properties": {},
            "style": {}
        }