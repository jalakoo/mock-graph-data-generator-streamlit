import streamlit as st
from constants import *
from pprint import pprint, pformat
from io import StringIO
import json
from models.mapping import Mapping
from logic.generate_csv import generate_csv

def generate_tab():
    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/fireworks.gif")
    with col2:
        st.write("Generate mock graph data from earlier mappings.")
    st.markdown("--------")

    mapping = st.session_state[MAPPINGS]
    export_folder = st.session_state[EXPORTS_PATH]

    st.write(f'CURRENT MAPPING: {len(mapping.nodes)} nodes and {len(mapping.relationships)} relationshps to generate.')
    with st.expander("Raw Mapping Data"):
        mapping_json = json.dumps(mapping.to_dict(), indent=4)
        st.code(mapping_json)

    st.markdown("--------")
    if st.button('Generate New Data', key=f'generate_data_button'):
        # TODO: Generate data from mapping
        generate_csv(
            mapping, 
            export_folder=export_folder)

        with st.expander("Generated Data"):
            st.write('tbd')
