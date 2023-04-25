# Now the new Generate Tab

import streamlit as st
import json
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander
import logging
from file_utils import load_string, save_file
from models.mapping import Mapping
import sys
import os
from logic.generate_mapping import mapping_from_json
from generate import generate_data, generate_zip
from datetime import datetime

# Convenience functions
# def import_file(file) -> bool:
#     if file is  None:
#         raise Exception(f'import.py: import_file function called with no file')

#     # Check if file is a valid JSON file
#     try:
#         json_file = json.loads(file)
#         # Bring in the raw import data for nodes and relationships
#         node_dicts = json_file["nodes"]
#         relationship_dicts = json_file["relationships"]
#         if node_dicts is None:
#             return False
#         if relationship_dicts is None:
#             return False

#         return True
#     except json.decoder.JSONDecodeError:
#         st.error(f'JSON file {file} is not valid.')
#         return False
#     except:
#         return False

# def file_selected(path):
#     selected_file = load_string(path)
#     # TODO: Should really check if it's a path object instead
#     try:
#         selected_filename = path.name
#     except:
#         head, tail = os.path.split(path)
#         selected_filename = tail
#     # Clear existing Mappings
#     st.session_state[MAPPINGS] = Mapping.empty()
#     # Update selected file data
#     st.session_state[IMPORTED_FILE] = selected_file
#     st.session_state[IMPORTED_FILENAME] = selected_filename
#     # Import
#     sucessful_import = import_file(selected_file)
#     if sucessful_import:
#         st.success(f"Import Complete.")
#     else:
#         st.error(f"Import Failed. Check file format.")

def import_tab():

    with st.expander("Instructions"):
        st.write(
            """
        1. Import or select a previously imported JSON file from an arrows.app export
        2. The mock graph data generator will automatically generate a .csv and .zip files
        3. Download the .zip file
        4. Proceed to the '③ Data Importer' tab
        """
        )
    

    st.markdown("--------")

    uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")
    if uploaded_file is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # To read file as string:
        current_file = stringio.read()

        # Save to session state
        st.session_state[MAPPINGS] = Mapping.empty()

        if current_file is not None:
            # TODO: Verfiy file is valid arrows JSON
            generators = st.session_state[GENERATORS]
            mapping = mapping_from_json(
                current_file, 
                generators)
            zip = generate_zip(mapping)
            st.download_button(
                label = "Download Zip file for Data Importer",
                data = zip,
                file_name = f"{uploaded_file.name}.zip",
                mime = "application/zip"
            )
