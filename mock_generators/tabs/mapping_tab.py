import streamlit as st
from constants import *
import json
import logging
from widgets.node_row import nodes_row
from widgets.relationship_row import relationship_row
from widgets.property_row import property_row
import uuid
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
import sys

empty_node_dict = {
    'id' : f'{str(uuid.uuid4())[:8]}',
    'labels' : [],
    'properties' : {
        "uuid":"string"
    },
    'caption' : '<new_node>',
    'position':{
        'x': 0,
        'y': 0
    }
}

empty_relationship_dict = {
    'id' : f'{str(uuid.uuid4())[:8]}',
    "type": "<new_type>",
    "style": {},
    "properties": {},
    "fromId": "",
    "toId": ""
}

def ignore_node(id: str)-> bool:
    raise Exception(f'Not implemented')

def delete_node(node: NodeMapping) -> bool:
    raise Exception(f'Not implemented')

def add_node(node: NodeMapping) -> bool:
    raise Exception(f'Not implemented')

def ignore_relationship(id: str)-> bool:
    try:
        mapping = st.session_state[MAPPINGS]
        mapping_relationships = mapping.relationships
        if id in mapping_relationships:
            del mapping_relationships[id]
            mapping.relationships = mapping_relationships
            st.session_state[MAPPINGS] = mapping
            return True
    except:
        logging.error(f'Problem excluding {type} relationship from mapping. ERROR: {sys.exc_info()[0]}')
        return False

def delete_relationship(rid: str) -> bool:
    try:
        # Delete the relationship from the mapping
        ignore_relationship(rid.id)
        # Delete from imported list
        relationships = st.session_state[IMPORTED_RELATIONSHIPS]
        relationships = [relationship for relationship in relationships if relationship.id != rid]
        st.session_state[IMPORTED_RELATIONSHIPS] = relationships
        logging.info(f'mapping_tab.py: Deleted relationship {rid} from imported list: {st.session_state[IMPORTED_RELATIONSHIPS]}')
        return True
    except:
        logging.error(f'Problem deleting relationship {rid}. ERROR: {sys.exc_info()[0]}')
        return False

def add_relationship(relationship: RelationshipMapping) -> bool:
    try:
        rid = relationship.id
        mapping = st.session_state[MAPPINGS]
        relationships = mapping.relationships
        relationships[rid] = relationship
        mapping.relationships = relationships
        st.session_state[MAPPINGS] = mapping
    except:
        logging.error(f'Problem adding relationship {relationship.id}. ERROR: {sys.exc_info()[0]}')
        return False
    return True

def mapping_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/shuffle.gif")
    with col2:
        st.write("Create and edit mock data generation options. \n\nExpand options for each node or relationship to edit labels, property names, and assign generator functions that will create mock property data. NOTE: ALL Nodes require a unique key property name to be selected.\n\nWhen finished, proceed to the Generate Tab to generate mock data.")

    # Load the raw imported nodes and relationship data (these are not the node and relationship mapping objects created from this imported data)
    nodes = st.session_state[IMPORTED_NODES]
    relationships = st.session_state[IMPORTED_RELATIONSHIPS]
    if nodes is None:
        nodes = []
    if relationships is None:
        relationships = []

    st.markdown("--------")

    st.subheader("**GLOBALS:**")
    # g1, g2, g3 = st.columns([3,3,1])
    # should_expand = False
    # with g1:
    #     include_globals = st.checkbox("Include Global Properties", value=False, help="Include global properties in data generation. These will currently overwrite any node local properties with the same property name.")
    # with g2:
    #     should_expand = st.checkbox("Expand All Rows", value=False, help="Automatically expand all row details")
    # with g3:
    num_global_properties = st.number_input("Number of Global Properties", min_value=0, value=0, help="Optional Properties added to ALL nodes and relationships. Will overwrite locally assigned Node or Relationship properties of the same name.")
        # num_global_properties = 0
        # add_global_button = st.button(f"➕ Add Global Property", key="mapping_add_global_button")
        # if add_global_button:
        #     num_global_properties += 1

    all_global_properties = []
    # if include_globals == True:
    for i in range(num_global_properties):
        global_property = property_row(
            type="global",
            id = f'',
            index = i,
            properties = []
        )
        all_global_properties.append(global_property)

    # Nodes
    st.markdown("--------")
    # TODO: Add ability to add ALL NODES ONLY properties

    n1, n2 = st.columns([6,1])
    with n1:
        st.subheader("**NODES:**")
    with n2:
        # TODO: Replace with an add button instead
        # num_nodes = st.number_input("Number:", min_value=0, value=len(nodes), key="mapping_number_of_nodes", help="Adjust the number of nodes to generate")

        add_node_button = st.button(f"➕ Add Node", key="mapping_add_node_button")
        if add_node_button:
            # Add an empty node dictionary to the existing nodes list
            nodes.append(empty_node_dict)
            st.experimental_rerun()

    if len(nodes) == 0:
        # Auto insert an empty node bc that's going to be the first thing someone is going to need to do.
        nodes.append(empty_node_dict)

    for i in range(len(nodes)):
        if i >= len(nodes):
             #Should never be out of index, but just in case
            raise Exception(f"Node index {i} out of range of raw node dictionary list: {nodes}")
        node_dict = nodes[i]
        # TODO: Add a callback for delete request?
        nodes_row(
            node_dict = node_dict,
            generators=st.session_state[GENERATORS], 
            # should_start_expanded=should_expand,
            additional_properties=all_global_properties)

    st.markdown("--------")
    r1, r2 = st.columns([6,1])
    with r1:
        st.subheader("**RELATIONSHIPS:**")
    # TODO: Add ability to add ALL RELATIONSHIPS ONLY properties
    with r2:
        # num_relationships = st.number_input("Number:", min_value=0, value=len(relationships), key="mapping_number_of_relationships", help="Adjust the number of relationships to generate")
        add_relationship_button = st.button(f"➕ Add Relationship", key="mapping_add_relationship_button")
        if add_relationship_button:
            # Add an empty node dictionary to the existing nodes list
            relationships.append(empty_node_dict)
            st.experimental_rerun()

    for i in range(len(relationships)):
        relationship_dict = None
        if i < len(relationships):
            relationship_dict = relationships[i]
        else:
            # Default new
            relationship_dict = empty_relationship_dict

        relationship_row(
            relationship = relationship_dict,
            generators=st.session_state[GENERATORS],
            # should_start_expanded=should_expand,
            additional_properties=all_global_properties)