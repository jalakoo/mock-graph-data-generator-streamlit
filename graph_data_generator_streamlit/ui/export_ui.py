

import streamlit as st
from graph_data_generator import generators
import graph_data_generator as gdg
from neo4j_uploader import upload, start_logging, stop_logging
import json

def export_ui():

    txt = st.session_state.get("JSON_CONFIG", None)
    if txt is None:
        st.error("Add JSON config to generate data")
        return

    # Generate data
    mapping = gdg.generate_mapping(txt)
    # zip = gdg.package(mapping)
    data = gdg.generate_dictionaries(mapping)

    with st.expander('Generated Data'):
        pretty = json.dumps(data, indent=4)
        st.code(pretty)
    
    st.markdown("**③ EXPORT**")

    c1, c2 = st.columns([1,1])
    with c1:
        with st.expander('Download .zip file'):

            st.markdown("That can be uploaded into [Neo4j's Data Importer](https://neo4j.com/docs/data-importer/current/)")
            
            # Create .zip file for data-importer
            filename = st.text_input("Name of file", value="mock_data", help="Name of file to be used for the.zip file. Ignored if pushing directly to a Neo4j database instance.")

            def on_download():
                st.session_state["DOWNLOADING"] == True

            try:
                zip = gdg.package(mapping)
                if zip is None:
                    st.warning('Unexpected problem generating file. Try an alternate JSON input')
                else:
                    st.download_button(
                        label = "Download .zip file",
                        data = zip,
                        file_name = f"{filename}.zip",
                        mime = "text/plain",
                        on_click = on_download
                    )
            except Exception as e:
                st.error(e)

    with c2:
        with st.expander("Upload to Neo4j"):

            uri = st.text_input(f'Neo4j URI', value = st.session_state["NEO4J_URI"], placeholder="neo4j+s//92bd05dc.databases.neo4j.io", help="URI for your Aura Neo4j instance")

            user = st.text_input(f'Neo4j USER', value = st.session_state["NEO4J_USER"], placeholder = "neo4j")

            password = st.text_input(f'Neo4j PASSWORD', type = "password", value = st.session_state["NEO4J_PASSWORD"])

            should_overwrite = st.toggle("Reset DB?", value=True)

            # Optionally upload generated data to Neo4j
            if st.button("Upload to Neo4j", help="Upload generated data to a Neo4j instance"):
                if uri is None or user is None or password is None:
                    st.error("Please specify the Neo4j instance credentials in the Configuration tab")
                    return 

                # Enable uploader logging
                start_logging()
                
                success = upload(neo4j_creds=(uri, user, password), data=data, should_overwrite=should_overwrite)
                if success == False:
                    st.warning("Upload failed. Please check your credentials and try again.")
                else:
                    st.info("Upload complete!")