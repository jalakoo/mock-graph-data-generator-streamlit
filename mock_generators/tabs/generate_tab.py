import streamlit as st
from constants import *
# from models.mapping import Mapping
from logic.generate_csv import generate_csv
from logic.generate_data_import import generate_data_importer_json
import os
import logging
import sys
import zipfile
from widgets.folder_files import folder_files_expander

def generate_tab():
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/fireworks.gif")
    with col2:
        st.write("Generate mock graph data.\n\nBe sure you're happy with the mocking options in the Mapping tab before running.")
    st.markdown("--------")

    mapping = st.session_state[MAPPINGS]
    export_folder = st.session_state[EXPORTS_PATH]
    zips_folder = st.session_state[ZIPS_PATH]

    st.write(f'CURRENT MAPPING: {len(mapping.nodes)} nodes and {len(mapping.relationships)} relationshps to generate.')
    with st.expander("Raw Mapping Data"):
        st.json(mapping.to_dict())

    st.markdown("--------")
    # should_clear = st.checkbox("Delete all files in export folder with each Generate run", value=True)

    # TODO: Add generated data report (counts and numbers?)
    # Number of each node type generated
    # Number of each relationship type generated
    # TODO: Move generated data to export
    g1, g2, g3 = st.columns(3)

    with g1:
        st.write(f'GENERATE DATA:')
        if st.button('FOR DATA-IMPORTER', key=f'generate_data_button'):

            # Stop if no mapping data available
            if len(mapping.nodes) == 0:
                st.error('No nodes to generate data for. Map at least one noded.')
                st.stop()
                return

            for key, node in mapping.nodes.items():
                # logging.info(f'Generating data for node: {node}')
                if len(node.properties) == 0:
                    st.error(f'Node {node.caption} has no properties. Add at least one property to generate data.')
                    st.stop()
                    return

            # Delete all files in export folder first
            dir = export_folder
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            # Data Importer Options
            success = generate_csv(
                mapping, 
                export_folder=export_folder)

            # Check that data was generated
            if success == False:
                st.error('Error generating data. Check console for details.')
                st.stop()
                return

            success = generate_data_importer_json(
                mapping,
                export_folder=export_folder,
                export_filename=DEFAULT_DATA_IMPORTER_FILENAME)

            # Check that data-import data was generated
            if success == False:
                st.error('Error generating data-import json. Check console for details.')
                st.stop()
                return

            try:
                with zipfile.ZipFile(f'{zips_folder}/{DEFAULT_DATA_IMPORTER_FILENAME}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # zipdir(export_folder, zipf)
                    path = export_folder
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file[0] =='.':
                                # Skip hidden files
                                continue
                            zipf.write(os.path.join(root, file), 
                                    os.path.relpath(os.path.join(root, file), 
                                                    os.path.join(path, '..')))
            except:
                st.error(f'Error creating zip file: {sys.exc_info()[0]}')
                st.stop()
                return

            if success == True:
                st.success('Data generated successfully.')

    with g2:
        st.write(f"GENERATED FILES:")
        folder_files_expander(export_folder)

    with g3:
        st.write(f'GENERATED ZIP FILES:')
        folder_files_expander(zips_folder)
