import streamlit as st
from constants import *
import json
import logging
from widgets.nodes import nodes_row
from widgets.relationships import relationship_row

def mapping_tab():

    st.write("Import, create, and edit mock data generation options.")
    uploaded_file = st.session_state[IMPORTED_FILE]
    if uploaded_file is not None:
        with st.expander("Imported File"):
            st.text(uploaded_file)
    st.markdown("--------")

    # Default options
    nodes = [{
        "id": "1",
        "labels": ["Person"],
        "caption": "",
        "properties": {
        }
    },
    {
        "id": "2",
        "labels": ["Company"],
        "caption": "",
        "properties": {
        }
    }]
    relationships = [{
        "id": "r1",
        "type": "",
        "fromId": "1",
        "toId": "2",
        "properties": {
        }
    }]

    # Convert uploaded file (if available) to json
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

    st.write("RELATIONSHIPS:")
    num_relationships = st.number_input("Number of relationships", min_value=1, value=len(relationships), key="mapping_number_of_relationships")
    for i in range(num_relationships):
        if i < len(relationships):
            relationship_row(relationships[i])
        else:
            relationship_row(None)