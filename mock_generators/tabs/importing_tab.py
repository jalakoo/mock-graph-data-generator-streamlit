# Now the new Generate Tab

import streamlit as st
from constants import *
from io import StringIO
from models.mapping import Mapping
from logic.generate_mapping import mapping_from_json
from generate import generate_zip

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

        name = uploaded_file.name.split(".")[0]
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
                file_name = f"{name}.zip",
                mime = "text/plain"
            )
