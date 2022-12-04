import streamlit as st
from constants import *

def export_tab():
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/export.gif")
    with col2:
        st.write(f"Export generated data.\n\nThe downloadable zip file can be uploaded into Neo4j's Data-Import tool. It contains all the files necessary to import the generated data into Neo4j.")
    st.markdown("--------")

    ec1, ec2 = st.columns(2)
    with ec1:
        st.write(f"Download generated file >")
        try:
            with open(f"{st.session_state[ZIPS_PATH]}/{DEFAULT_DATA_IMPORTER_FILENAME}.zip", "rb") as file:
                st.download_button(label="Download", data=file, file_name=f"{DEFAULT_DATA_IMPORTER_FILENAME}.zip", mime="application/zip", key=f"export_download_button")
        except:
            st.warning("No data-importer zip found. Please generate data first.")
    with ec2:
        st.write(f"Upload files to Neo4j:")
        link = '[Neo4j Aura Console](https://console.neo4j.io)'
        st.markdown(link, unsafe_allow_html=True)