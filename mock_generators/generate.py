import streamlit as st
from constants import *
from models.mapping import Mapping
from logic.generate_csv import generate_csv
from logic.generate_data_import import generate_data_importer_json
import os
import logging
import sys
import zipfile
from datetime import datetime

def generate_data(mapping: Mapping):

    export_folder = st.session_state[EXPORTS_PATH]
    zips_folder = st.session_state[ZIPS_PATH]
    imported_filename = st.session_state[IMPORTED_FILENAME]

    # TODO: Implement better filename cleaning
    # TODO: Breaks when using a copy and pasted file
    export_zip_filename = f'{imported_filename}'.lower()
    export_zip_filename = export_zip_filename.replace(".json", "")
    export_zip_filename.replace(" ", "_")
    export_zip_filename.replace(".", "_")

    # Stop if no mapping data available
    if len(mapping.nodes) == 0:
        st.error('No nodes to generate data for. Map at least one noded.')
        st.stop()
        return

    # Generate values from mappings
    for _, node in mapping.nodes.items():
        # logging.info(f'Generating data for node: {node}')
        if len(node.properties) == 0:
            st.error(f'Node {node.caption} has no properties. Add at least one property to generate data.')
            st.stop()
            return
        node.generate_values()

    for _, rel in mapping.relationships.items():
        rel.generate_values()

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
        # st.stop()
        # return

    success = generate_data_importer_json(
        mapping,
        export_folder=export_folder,
        export_filename=DEFAULT_DATA_IMPORTER_FILENAME)

    # Check that data-import data was generated
    if success == False:
        st.error('Error generating data-import json. Check console for details.')
        # st.stop()
        # return

    # Only attempt to zip files if data generation was successful
    if success:
        try:
            # Create zip file, appended with time created
            # now = str(datetime.now().isoformat())
            zip_path = f'{zips_folder}/{export_zip_filename}.zip'
            logging.info(f'generate_tab: Creating zip file: {zip_path}')
            with zipfile.ZipFile(f'{zip_path}', 'w', zipfile.ZIP_DEFLATED) as zipf:
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
            # st.stop()
            return

    if success == True:
        st.success('Data generated successfully.')
