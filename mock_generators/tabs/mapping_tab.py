import streamlit as st
from constants import *
import json
import logging
from widgets.node_row import nodes_row
from widgets.relationship_row import relationship_row
from widgets.property_row import property_row

def mapping_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/shuffle.gif")
    with col2:
        st.write("Create and edit mock data generation options. \n\nExpand options for each node or relationship to edit labels, property names, and assign generator functions that will create mock property data. NOTE: ALL Nodes require a unique key property name to be selected.\n\nWhen finished, proceed to the Generate Tab to generate mock data.")

    nodes = st.session_state[IMPORTED_NODES]
    relationships = st.session_state[IMPORTED_RELATIONSHIPS]
    if nodes is None:
        nodes = []
    if relationships is None:
        relationships = []

    st.markdown("--------")

    st.subheader("**GLOBALS:**")
    g1, g2, g3 = st.columns([3,3,1])
    should_expand = False
    with g1:
        include_globals = st.checkbox("Include Global Properties", value=False, help="Include global properties in data generation. These will currently overwrite any node local properties with the same property name.")
    with g2:
        should_expand = st.checkbox("Expand All Rows", value=False, help="Automatically expand all row details")
    with g3:
        num_global_properties = st.number_input("Number of Global Properties", min_value=0, value=0, help="Optional Properties added to ALL nodes and relationships. Will overwrite locally assigned Node or Relationship properties of the same name.")
    all_global_properties = []
    if include_globals == True:
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
        num_nodes = st.number_input("Number:", min_value=0, value=len(nodes), key="mapping_number_of_nodes", help="Adjust the number of nodes to generate")
    for i in range(num_nodes):
        node_dict = None
        if i < len(nodes):
            node_dict = nodes[1]
        nodes_row(
            node_dict = node_dict,
            generators=st.session_state[GENERATORS], 
            should_start_expanded=should_expand,
            additional_properties=all_global_properties)

    st.markdown("--------")
    r1, r2 = st.columns([6,1])
    with r1:
        st.subheader("**RELATIONSHIPS:**")
    # TODO: Add ability to add ALL RELATIONSHIPS ONLY properties
    with r2:
        num_relationships = st.number_input("Number:", min_value=0, value=len(relationships), key="mapping_number_of_relationships", help="Adjust the number of relationships to generate")
    for i in range(num_relationships):
        relationship_dict = None
        if i < len(relationships):
            relationship_dict = relationships[i]
        relationship_row(
            relationship = relationship_dict,
            generators=st.session_state[GENERATORS],
            should_start_expanded=should_expand,
            additional_properties=all_global_properties)