import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header

def data_importer_tab():
    is_local = st.checkbox("Use HTTP", value=False, help="Select Use HTTP if connecting with a local Neo4j instance.")

    if is_local == True:
        components.iframe("http://data-importer.graphapp.io/", height=1000, scrolling=False)    
    else:
        components.iframe("https://data-importer.graphapp.io/", height=1000, scrolling=False)