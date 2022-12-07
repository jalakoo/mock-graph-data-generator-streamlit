import streamlit as st
from constants import *
from widgets.folder_files import folder_files_expander

def export_tab():
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/export.gif")
    with col2:
        st.write(f"Export generated data.\n\nAll generated files are listed in the Generated Files section below. NOTE: These files are wiped from the export files folder whenever the generate button from the Generate Tab is clicked. The downloadable zip files from the Generated Zip Files section can be uploaded into [Neo4j's Data-Import tool](https://console.neo4j.io). It contains all the files necessary to import the generated data into Neo4j.")
    st.markdown("--------")

    export_folder = st.session_state[EXPORTS_PATH]
    zips_folder = st.session_state[ZIPS_PATH]

    ec1, ec2, ec3 = st.columns(3)

    with ec1:
        st.write(f"GENERATED FILES:")
        folder_files_expander(export_folder, widget_id="export_tab")

    with ec2:
        st.write(f'(1) GENERATED ZIP FILES:')
        folder_files_expander(zips_folder, widget_id="export_tab", enable_download=True, enable_delete_button=True)

    with ec3:
        st.write(f"(2) Upload desired .zip file to Neo4j:")
        link = '[Neo4j Aura Console](https://console.neo4j.io)'
        st.markdown(link, unsafe_allow_html=True)