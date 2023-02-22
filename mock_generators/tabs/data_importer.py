import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from constants import *

def data_importer_tab():

    # col1, col2 = st.columns([1,11])
    # with col1:
    #     st.image("mock_generators/media/export.gif")
    #     # st.image("mock_generators/media/signpost.gif")
    # with col2:
    #     st.write(f"Data Importer App.\n\nUse the [Data Importer Tool](https://data-importer.graphapp.io/) to upload generated .zip file to for review and ingesetion to a Neo4j database instance.")
    with st.expander('Instructions'):
        st.write("""
        1. Connect to your Neo4j instance
        2. Click on the '...' options button in the Data Importer header
        3. Select 'Open model (with data)'
        4. Select the .zip file with the generated data
        5. Click the 'Run import' button
        """)
    with st.expander("Options"):
        is_local = st.checkbox("Use HTTP", value=False, help="Select Use HTTP if connecting with a local Neo4j instance.")
    st.markdown("--------")

    if is_local == True:
        components.iframe("http://data-importer.graphapp.io/", height=1000, scrolling=False)    
    else:
        components.iframe("https://data-importer.graphapp.io/", height=1000, scrolling=False)