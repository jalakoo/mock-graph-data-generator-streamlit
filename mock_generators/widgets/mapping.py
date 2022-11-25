import streamlit as st
from constants import *

def mapping_tab():

    st.write("Import, create, and edit mock data generation options.")
    uploaded_file = st.session_state[IMPORTED_FILE]
    if uploaded_file is not None:
        with st.expander("Imported File"):
            st.text(uploaded_file)
    st.markdown("--------")

