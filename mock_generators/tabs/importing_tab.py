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
from generate import generate_data
from datetime import datetime

# Convenience functions
def import_file(file) -> bool:
    if file is  None:
        raise Exception(f'import.py: import_file function called with no file')

    # Check if file is a valid JSON file
    try:
        json_file = json.loads(file)
        # Bring in the raw import data for nodes and relationships
        node_dicts = json_file["nodes"]
        relationship_dicts = json_file["relationships"]
        if node_dicts is None:
            return False
        if relationship_dicts is None:
            return False

        return True
    except json.decoder.JSONDecodeError:
        st.error(f'JSON file {file} is not valid.')
        return False
    except:
        return False

def file_selected(path):
    selected_file = load_string(path)
    # TODO: Should really check if it's a path object instead
    try:
        selected_filename = path.name
    except:
        head, tail = os.path.split(path)
        selected_filename = tail
    # Clear existing Mappings
    st.session_state[MAPPINGS] = Mapping.empty()
    # Update selected file data
    st.session_state[IMPORTED_FILE] = selected_file
    st.session_state[IMPORTED_FILENAME] = selected_filename
    # Import
    sucessful_import = import_file(selected_file)
    if sucessful_import:
        st.success(f"Import Complete.")
    else:
        st.error(f"Import Failed. Check file format.")

def import_tab():

    # col1, col2 = st.columns([1,11])
    # with col1:
    #     # st.image("mock_generators/media/import.gif")
    #     st.image("mock_generators/media/fireworks.gif")
    # with col2:
    #     st.markdown("Import JSON files from an [arrows.app](https://arrows.app/#/local/id=A330UT1VEBAjNH1Ykuss) data model. \n\nProceed to the Mapping Tab when complete.")

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

    i1, i2, i3 = st.columns(3)

    start_generated = datetime.now()
    last_generated = start_generated

    with i1:
        # File Selection
        st.write('SELECT ARROWS FILE:')
        # st.markdown("--------")

        selected_file = None
        import_option = st.radio("Select Import Source", ["An Existing File", "Upload"], horizontal=True)

        if import_option == "An Existing File":
            # Saved options
            st.write("Select an import file:")

            folder_files_expander(
                folder_path=st.session_state[IMPORTS_PATH], file_selected=file_selected, 
                specific_extension=".json",
                file_selection_button_text="Load this file")

        elif import_option == "Upload":
            # Upload a new file
            uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")
            if uploaded_file is not None:
                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                # To read file as string:
                selected_file = stringio.read()

                # Save to import folder
                selected_filepath = f"{st.session_state[IMPORTS_PATH]}/{uploaded_file.name}"
                try:
                    save_file(
                        filepath=selected_filepath,
                        data=selected_file)
                except:
                    st.error(f"Error saving file to {st.session_state[IMPORTS_PATH]}")
                    logging.error(f'Error saving file: {sys.exc_info()[0]}')
                
                file_selected(selected_filepath)
        else:
            logging.info(f'Copy & Paste Option disabled') 


        # Process uploaded / selected file
        current_file = st.session_state[IMPORTED_FILE]
        if current_file is not None:
            # Verfiy file is valid arrows JSON
            try:
                generators = st.session_state[GENERATORS]
                mapping = mapping_from_json(
                    current_file, 
                    generators)
                # st.session_state[MAPPINGS] = mapping
                generate_data(mapping)

                last_generated = datetime.now()
                # st.success(f"New data generated from import file.")

            except json.decoder.JSONDecodeError:
                st.error('Import JSON file is not valid.')
            except Exception as e:
                st.error(f'Uncaught Error: {e}')

    with i2:
        export_folder = st.session_state[EXPORTS_PATH]
        st.write(f"RECENTLY GENERATED FILES:")
        if start_generated != last_generated:
            st.success(f"New data generated from import file.")
        folder_files_expander(export_folder, widget_id="export_tab", enable_download=True)

    with i3:

        st.write('GENERATED ZIP FILES:')
        if start_generated != last_generated:
            st.success(f"New zip files generated from import file.")
        zips_folder = st.session_state[ZIPS_PATH]       
        
        folder_files_expander(zips_folder, widget_id="export_tab", enable_download=True, enable_delete_button=True)