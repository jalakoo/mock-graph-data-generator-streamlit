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

    # Convert uploaded file (if available) to json
    if uploaded_file is not None:
        try:
            json_file = json.loads(uploaded_file)
            nodes = json_file["nodes"]
            # relationships = json_file["relationships"]
            # logging.info(f"Successfully converted uploaded file to json: {json_file}\n\nnodes: {nodes} - count: {len(nodes)}")
            for node in nodes:
                nodes_row(node)
        except json.decoder.JSONDecodeError:
            st.error('JSON file is not valid.')