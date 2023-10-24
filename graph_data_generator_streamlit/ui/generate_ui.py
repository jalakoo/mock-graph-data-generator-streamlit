# Now the new Generate Tab

import streamlit as st
from graph_data_generator import generators
import graph_data_generator as gdg
from managers.n4j_manager import upload_data
import json


def neo4j_config():
    # NEO4J URI
    neo4j_uri = st.secrets.get("NEO4J_URI", None)
    if neo4j_uri is None or neo4j_uri == "":
        neo4j_uri = st.session_state.get("NEO4J_URI", None)
    else:
        st.session_state["NEO4J_URI"] = neo4j_uri

    new_neo4j_uri = st.text_input(f'Neo4j URI', value = neo4j_uri, placeholder="92bd05dc.databases.neo4j.io", help="URI for your Aura Neo4j instance minus the protocol")
    if new_neo4j_uri != neo4j_uri:
        st.session_state["NEO4J_URI"] = new_neo4j_uri

    # NEO4J USER
    neo4j_user = st.secrets.get("NEO4J_USER", None)
    if neo4j_user is None or neo4j_user == "":
        neo4j_user = st.session_state.get("NEO4J_USER", None)
    else:
        st.session_state["NEO4J_USER"] = neo4j_user
    
    new_neo4j_user = st.text_input(f'Neo4j USER', value = neo4j_user, placeholder = "neo4j")
    if new_neo4j_uri != neo4j_user:
        st.session_state["NEO4J_USER"] = new_neo4j_user

    # NEO4J PASSWORD
    neo4j_pass = st.secrets.get("NEO4J_PASSWORD", None)
    if neo4j_pass is None or neo4j_pass == "":
        neo4j_pass = st.session_state.get("NEO4J_PASSWORD", None)
    else:
        st.session_state["NEO4J_PASSWORD"] = neo4j_pass

    new_neo4j_pass = st.text_input(f'Neo4j PASSWORD', type = "password", value = neo4j_pass)
    if new_neo4j_pass != neo4j_pass:
        st.session_state["NEO4J_PASSWORD"] = new_neo4j_pass

def generate_ui():

    sample = None
    if st.button('Load Sample'):
        sample_raw = json.load(open("graph_data_generator_streamlit/samples/minimal.json"))
        sample = json.dumps(sample_raw, indent=4)


    txt = st.text_area("Paste .JSON config below", height=500, help="Click out of the text area to generate the .zip file.", value=sample)
    if txt is None or txt == "":
        return

    mapping = gdg.generate_mapping(txt)

    st.markdown("**③ EXPORT**")

    c1, c2 = st.columns([1,1])
    with c1:
        with st.expander('Download .zip file'):
            # Create .zip file for data-importer
            filename = st.text_input("Name of file", value="mock_data", help="Name of file to be used for the.zip file. Ignored if pushing directly to a Neo4j database instance.")
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
        with st.expander("Upload to Neo4j"):
            neo4j_config()

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