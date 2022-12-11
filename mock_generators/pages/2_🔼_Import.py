import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander
import logging
from file_utils import load_string, save_file
from models.mapping import Mapping
import sys

# SETUP
st.set_page_config(
    layout="wide",
    page_title="Import"
)
if IMPORTS_PATH not in st.session_state:
    st.session_state[IMPORTS_PATH] = DEFAULT_IMPORTS_PATH
if IMPORTED_FILE not in st.session_state:
    st.session_state[IMPORTED_FILE] = None

# UI
header(
    title=IMPORT_PAGE_TITLE,
    description=f'Load or import an arrows.json file to use as a starting point for creating interconnected mock graph data.',
    color_name="Orange",
    prior_page="Design",
    next_page="Properties"
)

selected_file = None
import_option = st.radio("Import Type", ["An Existing File", "New Upload"], horizontal=True)

st.markdown("--------")

if import_option == "An Existing File":
    # Saved options
    st.write("Select an import file:")
    def file_selected(path):
        selected_file = load_string(path)
        selected_filename = path.name
        # Clear existing Mappings
        st.session_state[MAPPINGS] = Mapping.empty()
        # Update selected file data
        st.session_state[IMPORTED_FILE] = selected_file
        st.session_state[IMPORTED_FILENAME] = selected_filename
        st.success(f"Import Complete. Proceed to the Properties page")

    folder_files_expander(folder_path=st.session_state[IMPORTS_PATH], file_selected=file_selected, file_selection_button_text="Select this file")

else:
    # Upload a new file
    uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")
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

# with i2:
#     # Process uploaded / selected file
#     current_file = st.session_state[IMPORTED_FILE]
#     if current_file is not None:
#         # TODO: Verfiy file is valid arrows JSON

#         # Write data to the imports folder


#         # TODO: Update this to read from the appropriate file from the new imports folder

#         st.write(f"[3]  Using {st.session_state[IMPORTED_FILENAME]} contents:")
#         st.text(current_file)