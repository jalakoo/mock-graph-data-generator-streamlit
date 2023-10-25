# Now the new Generate Tab

import streamlit as st
from graph_data_generator import generators
import graph_data_generator as gdg
from managers.n4j_manager import upload_data
import json
import pyclip

def generate_ui():

    if st.session_state["ARROWS_DICT"] is not None:
        dict = st.session_state.get("ARROWS_DICT", {}).get('graph', None)
        string = json.dumps(dict, indent=4)
        st.session_state["JSON_CONFIG"] = string
    if st.button('Load Sample'):
        sample_raw = json.load(open("graph_data_generator_streamlit/samples/minimal.json"))
        prior = json.dumps(sample_raw, indent=4)
        st.session_state["JSON_CONFIG"] = prior

    txt = st.text_area("Enter .JSON config below", height=500, help="Click out of the text area to generate the .zip file.", value=st.session_state.JSON_CONFIG)