import streamlit as st
import json
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander
import logging
from file_utils import load_string, save_file
from models.mapping import Mapping
import sys

def import_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/import.gif")
    with col2:
        st.markdown("Import JSON files from an [arrows.app](https://arrows.app/#/local/id=A330UT1VEBAjNH1Ykuss) data model. \n\nProceed to the Mapping Tab when complete.")

    st.markdown("--------")

    i1, i2 = st.columns(2)

    with i1:
        selected_file = None
        # st.header(f'[1] Select Import Source')
        import_option = st.radio("[1] Select Import Source", ["An Existing File", "Upload"])

        st.markdown("--------")

        if import_option == "An Existing File":
            # Saved options
            st.write("[2]  Select an import file:")
            def file_selected(path):
                selected_file = load_string(path)
                selected_filename = path.name
                # Clear existing Mappings
                st.session_state[MAPPINGS] = Mapping.empty()
                # Update selected file data
                st.session_state[IMPORTED_FILE] = selected_file
                st.session_state[IMPORTED_FILENAME] = selected_filename
                st.success(f"Import Complete")

            folder_files_expander(folder_path=st.session_state[IMPORTS_PATH], file_selected=file_selected, file_selection_button_text="Select this file")

        else:
            # Upload a new file
            uploaded_file = st.file_uploader("[2]  Upload an arrows JSON file", type="json")
            if uploaded_file is not None:
                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                # To read file as string:
                selected_file = stringio.read()

                # Save to import folder
                try:
                    save_file(
                        filepath=f"{st.session_state[IMPORTS_PATH]}/{uploaded_file.name}",
                        data=selected_file)
                except:
                    st.error(f"Error saving file to {st.session_state[IMPORTS_PATH]}")
                    logging.error(f'Error saving file: {sys.exc_info()[0]}')
                
                # Clear existing Mappings
                st.session_state[MAPPINGS] = Mapping.empty()

                # Set file data
                st.session_state[IMPORTED_FILENAME] = uploaded_file.name
                st.session_state[IMPORTED_FILE] = selected_file

                st.success(f"Import Complete")

    with i2:
        # Process uploaded / selected file
        current_file = st.session_state[IMPORTED_FILE]
        if current_file is not None:
            # TODO: Verfiy file is valid arrows JSON

            # Write data to the imports folder


            # TODO: Update this to read from the appropriate file from the new imports folder

            st.write(f"[3]  Using {st.session_state[IMPORTED_FILENAME]} contents:")
            st.text(current_file)