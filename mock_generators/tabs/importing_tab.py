import streamlit as st
import json
from constants import *
from io import StringIO
from widgets.folder_files import folder_files_expander

def import_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/import.gif")
    with col2:
        st.markdown("Optionally import JSON files from an [arrows.app](https://arrows.app/#/local/id=A330UT1VEBAjNH1Ykuss) data model for use in the mapping tab.")

    st.markdown("--------")

    i1, i2 = st.columns(2)

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
        uploaded_file = st.file_uploader("Upload an arrows JSON file", type="json")

        if uploaded_file is not None:
            # To read file as bytes:
            # bytes_data = uploaded_file.getvalue()
            # st.write(bytes_data)

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

            # To read file as string:
            imported_file = stringio.read()

            # TODO: Verfiy file is valid arrows JSON

            # Write data to the imports folder


            # TODO: Update this to read from the appropriate file from the new imports folder

            # Retain the imported data for later use
            if imported_file is not None and imported_file != st.session_state[IMPORTED_FILE]:
                st.session_state[IMPORTED_FILE] = imported_file

        imported_file = st.session_state[IMPORTED_FILE]
        if imported_file is not None:
            st.markdown("--------")
            st.write("Imported file:")
            st.text(imported_file)
            st.session_state[IMPORTED_FILE] = imported_file

        st.write("Or select a previously imported file:")

        
        
        # TODO: Support copy & paste json



