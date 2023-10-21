# Now the new Generate Tab

import streamlit as st
from graph_data_generator import generators
import graph_data_generator as gdg
from managers.n4j_manager import upload_data
import json

def generate_ui():

    st.write("Copy & Paste Arrows.app .JSON file")
    filename = st.text_input("Name of file", value="mock_data")
    txt = st.text_area("Paste arrows.app JSON here", height=500, help="Click out of the text area to generate the .zip file.")
    if txt is None or txt == "":
        return

    mapping = gdg.generate_mapping(txt)

    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        # Create .zip file for data-importer
        try:
            zip = gdg.package(mapping)
            if zip is None:
                st.warning('Unexpected problem generating file. Try an alternate JSON input')
            else:
                st.download_button(
                    label = "Download .zip file",
                    data = zip,
                    file_name = f"{filename}.zip",
                    mime = "text/plain"
                )
        except Exception as e:
            st.error(e)

    with c2:
        # Optionally upload generated data to Neo4j
        if st.button("Upload to Neo4j", help="Upload generated data to a Neo4j instance"):
            uri = st.session_state.get("NEO4J_URI", None)
            user = st.session_state.get("NEO4J_USER", None)
            password = st.session_state.get("NEO4J_PASSWORD", None)
            if uri is None or user is None or password is None:
                st.error("Please specify the Neo4j instance credentials in the Configuration tab")
                return 
            data = gdg.generate_dictionaries(mapping)
            # json_string = json.dumps(data)
            # print(f'Generated dictionary data: {json_string}')
            upload_data(creds=(uri, user, password), data=data)