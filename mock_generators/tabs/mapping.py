import streamlit as st
from constants import *
import json
import logging
from widgets.node_row import nodes_row
from widgets.relationship_row import relationship_row

def mapping_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/shuffle.gif")
    with col2:
        st.write("Create and edit mock data generation options. \n\nNodes and relationships are default INCLUDED from mapping, meaning data will be generated.  Expand options for each node or relationship > verify/edit labels and properties > optionally exclude from generation.")
    uploaded_file = st.session_state[IMPORTED_FILE]
    if uploaded_file is not None:
        with st.expander("Imported File"):
            st.text(uploaded_file)
    st.markdown("--------")

    # Default options
    # Matching arrows.json dict format
    nodes = [
        {
        "id": "n0",
        "position":{
            "x": 0,
            "y": 0
        },
        "caption": "Person",
        "labels": [],
        "properties": {
            "uuid": "string",
            "name": "string",
        }
    },
    {
        "id": "n1",
        "position":{
            "x": 200,
            "y": 200
        },
        "caption": "Company",
        "labels": [],
        "properties": {
            "uuid":"string",
            "name": "string",
        }
    }]
    relationships = [{
        "id": "n0",
        "type": "WORKS_AT",
        "fromId": "n0",
        "toId": "n1",
        "properties": {
        }
    }]

    # Convert uploaded file (if available) to json
    # Supporting arrows 0.5.4
    if uploaded_file is not None:
        try:
            json_file = json.loads(uploaded_file)
            nodes = json_file["nodes"]
            relationships = json_file["relationships"]
            
        except json.decoder.JSONDecodeError:
            st.error('JSON file is not valid.')

    st.write("NODES:")
    num_nodes = st.number_input("Number of nodes", min_value=1, value=len(nodes), key="mapping_number_of_nodes")
    for i in range(num_nodes):
        if i < len(nodes):
            nodes_row(nodes[i])
        else:
            nodes_row(None)

    st.markdown("--------")
    st.write("RELATIONSHIPS:")
    num_relationships = st.number_input("Number of relationships", min_value=1, value=len(relationships), key="mapping_number_of_relationships")
    for i in range(num_relationships):
        if i < len(relationships):
            relationship_row(relationships[i])
        else:
            relationship_row(None)