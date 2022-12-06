import streamlit as st
import json
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander
import logging
from file_utils import load_string

def import_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/import.gif")
    with col2:
        st.markdown("Optionally import JSON files from an [arrows.app](https://arrows.app/#/local/id=A330UT1VEBAjNH1Ykuss) data model for use in the mapping tab.")

    st.markdown("--------")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.write("Sample Import file:")
        try:
            with open(DEFAULT_ARROWS_SAMPLE_PATH) as input:
                generators_file = input.read()
        except FileNotFoundError:
            st.error('File not found.')
        with st.expander("Arrows JSON Sample"):
            st.text(generators_file)

    with i2:
        selected_file = None
        uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")
        if uploaded_file is not None:
            # To convert to a string based IO:
            stringio = StringIO(selected_file.getvalue().decode("utf-8"))
            # To read file as string:
            selected_file = stringio.read()
            st.session_state[IMPORTED_FILE] = selected_file

        st.write("Or select a previously imported file:")
        def file_selected(path):
            selected_file = load_string(path)
            st.session_state[IMPORTED_FILE] = selected_file
            st.success(f"Loaded file: {path.name}")

        folder_files_expander(folder_path=st.session_state[IMPORTS_PATH], file_selected=file_selected)

        with i3:
            # Process uploaded / selected file
            current_file = st.session_state[IMPORTED_FILE]
            if current_file is not None:
                # TODO: Verfiy file is valid arrows JSON

                # Write data to the imports folder


                # TODO: Update this to read from the appropriate file from the new imports folder

                st.write("Using file:")
                st.text(current_file)
