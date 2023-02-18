import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from constants import *

def data_importer_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/export.gif")
        # st.image("mock_generators/media/signpost.gif")
    with col2:
        st.write(f"Data Importer App.\n\nUse the [Data Importer Tool](https://data-importer.graphapp.io/) to upload generated .zip file to for review and ingesetion to a Neo4j database instance.")
    st.markdown("--------")

    components.iframe("https://data-importer.graphapp.io/", height=1000, scrolling=False)