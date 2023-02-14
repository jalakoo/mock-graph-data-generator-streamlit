import streamlit as st
import json
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander
import logging
from file_utils import load_string, save_file
from models.mapping import Mapping
import sys
import datetime
import os
from logic.generate_mapping import mapping_from_json

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

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/import.gif")
    with col2:
        st.markdown("Import JSON files from an [arrows.app](https://arrows.app/#/local/id=A330UT1VEBAjNH1Ykuss) data model. \n\nProceed to the Mapping Tab when complete.")

    st.markdown("--------")

    i1, i3 = st.columns([3,3])

    with i1:
        # File Selection

        selected_file = None
        import_option = st.radio("Select Import Source", ["An Existing File", "Upload"], horizontal=True)

        st.markdown("--------")

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
        # else:
            # # Copy & Paste
            # pasted_json = st.text_area("Paste an arrows JSON file here", height=300)
            # # logging.info(f'pasted_json: {pasted_json}')
            # if pasted_json is not None and pasted_json != "":
            #     temp_filename = f'pasted_file.json'
            #     selected_filepath = f"{st.session_state[IMPORTS_PATH]}/{temp_filename}"
            #     # data = json.dumps(pasted_json, indent=4)
            #     try:
            #         save_file(
            #             filepath=selected_filepath,
            #             data=pasted_json)
            #     except:
            #         st.error(f"Error saving file to {st.session_state[IMPORTS_PATH]}")
            #         logging.error(f'Error saving file: {sys.exc_info()[0]}')
                
            #     file_selected(selected_filepath)

    # with i2:

    #     # Display loaded file
    #     st.write('IMPORT STATUS:')

    #     # Process uploaded / selected file
        current_file = st.session_state[IMPORTED_FILE]
        if current_file is not None:
            # Verfiy file is valid arrows JSON
            try:
                generators = st.session_state[GENERATORS]
                mapping = mapping_from_json(current_file, generators)
                st.session_state[MAPPINGS] = mapping
                st.success(f"Mappings generated from import file.")

            except json.decoder.JSONDecodeError:
                st.error('Import JSON file is not valid.')
            except Exception as e:
                st.error(f'Uncaught Error: {e}')
    #     else:
    #         st.warning(f'No file selected. Please select a file to import.')

    with i3:
        # Display auto-generated Mapping files
        st.write('MAPPING DATA:')
        mapping = st.session_state[MAPPINGS]
        if mapping is None:
            st.warning(f'No mapping data available. Import a file.')
        elif mapping.is_empty() == True:
            st.error(f'No mapping data extracted from imported file. Is the file correctly formatted?')
        elif mapping.is_valid() == False:
            st.error(f'Mappping invalid. Please check the imported file.')
        else:
            st.success(f'Mappping options valid for generation. Proceed to Generate Tab.')

            # For the curious
            with st.expander("Raw Mapping Data"):
                if mapping is not None:
                    st.json(mapping.to_dict())