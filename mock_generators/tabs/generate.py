import streamlit as st
from constants import *
# from models.mapping import Mapping
from logic.generate_csv import generate_csv
from logic.generate_data_import import generate_data_importer_json
import os
import logging

def generate_tab():
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/fireworks.gif")
    with col2:
        st.write("Generate mock graph data from earlier mappings.")
    st.markdown("--------")

    mapping = st.session_state[MAPPINGS]
    export_folder = st.session_state[EXPORTS_PATH]

    st.write(f'CURRENT MAPPING: {len(mapping.nodes)} nodes and {len(mapping.relationships)} relationshps to generate.')
    with st.expander("Raw Mapping Data"):
        st.json(mapping.to_dict())

    st.markdown("--------")
    # should_clear = st.checkbox("Delete all files in export folder with each Generate run", value=True)
    if st.button('Generate New Data', key=f'generate_data_button'):

        # Stop if no mapping data available
        if len(mapping.nodes) == 0:
            st.error('No nodes to generate data for. Map at least one noded.')
            st.stop()
            return

        for key, node in mapping.nodes.items():
            logging.info(f'Generating data for node: {node}')
            if len(node.properties) == 0:
                st.error(f'Node {node.caption} has no properties. Add at least one property to generate data.')
                st.stop()
                return

        # Data Importer Options
        generate_csv(
            mapping, 
            export_folder=export_folder)

        generate_data_importer_json(
            mapping,
            export_folder=export_folder)

        # TODO: Cypher Options



    st.markdown("--------")
    st.write(f"FILES IN EXPORT FOLDER:")
    try:
        for root, dirs, files in os.walk(st.session_state[EXPORTS_PATH]):
            for file in files:
                with st.expander(file):
                    with open(os.path.join(root, file), 'r') as f:
                        st.text(f.read())
    except:
        st.error(f'Could not retrieve files from export folder path: {export_folder}')
