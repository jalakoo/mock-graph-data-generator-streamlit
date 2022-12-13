import streamlit as st
from widgets.header import header
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander
import logging
from file_utils import load_string, save_file
from models.mapping import Mapping
import sys
import json
from widgets.default_state import load_state

# SETUP
st.set_page_config(
    layout="wide",
    page_title="Import"
)
load_state()


# Convenience functions
def file_selected(path):
    selected_file = load_string(path)
    selected_filename = path.name
    # Clear existing Mappings
    st.session_state[MAPPINGS] = Mapping.empty()
    # Update selected file data
    st.session_state[IMPORTED_FILE] = selected_file
    st.session_state[IMPORTED_FILENAME] = selected_filename
    # Import
    sucessful_import = import_file(selected_file)
    if sucessful_import:
        st.success(f"Import Complete. Proceed to the Mapping page")
    else:
        st.error(f"Import Failed. Please try again.")

def import_file(file) -> bool:
    if file is  None:
        raise Exception(f'import.py: import_file function called with no file')

    try:
        json_file = json.loads(file)
        # Bring in the raw import data for nodes and relationships
        node_dicts = json_file["nodes"]
        relationship_dicts = json_file["relationships"]
        if node_dicts is None:
            node_dicts = []
        if relationship_dicts is None:
            relationship_dicts = []
        
        st.session_state[IMPORTED_NODES] = node_dicts
        st.session_state[IMPORTED_RELATIONSHIPS] = relationship_dicts
        return True
    except json.decoder.JSONDecodeError:
        st.error(f'JSON file {file} is not valid.')
        return False
    except:
        return False


# UI
header(
    title=IMPORT_PAGE_TITLE,
    description=f'Load or import an arrows.json file to use as a starting point for creating interconnected mock graph data.',
    color_name="Orange",
    prior_page="Design",
    next_page="Mapping"
)

i1, i2 = st.columns([2,1])
with i1:
    # Select Import Type
    selected_file = None
    import_option = st.radio("Import Type", ["An Existing File", "New Upload"], horizontal=True)

    st.markdown("--------")

    # TODO: Add ability to optionally merge with existing mappings
    if import_option == "An Existing File":
        # Saved options
        st.write("Select an import file:")
        folder_files_expander(folder_path=st.session_state[IMPORTS_PATH], file_selected=file_selected, file_selection_button_text="User this file")

    else:
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

    # TODO: Display general imported data
    with i2:
        nodes = st.session_state[IMPORTED_NODES]
        relationships = st.session_state[IMPORTED_RELATIONSHIPS]
        if len(nodes) > 0 or len(relationships) > 0:
            st.write(f"Imported Data:")
            st.write(f"- {len(nodes)} imported nodes")
            st.write(f"- {len(relationships)} imported relationships")


# For displaying loaded data
# with i2:
#     # Process uploaded / selected file
#     current_file = st.session_state[IMPORTED_FILE]
#     if current_file is not None:
#         # TODO: Verfiy file is valid arrows JSON
#         # TODO: Update this to read from the appropriate file from the new imports folder
#         st.write(f"[3]  Using {st.session_state[IMPORTED_FILENAME]} contents:")
#         st.text(current_file)