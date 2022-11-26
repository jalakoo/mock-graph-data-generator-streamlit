import streamlit as st
from constants import *
from file_utils import load_json, load_string
from models.generator import Generator, generators_from_json

def config_tab() -> list[Generator]:

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/options.gif")
    with col2:
        st.write("Optionally change the source locations for importing and reading generator specifications and code files.")
    st.markdown("--------")


    new_spec_filepath = st.text_input("Generators Spec filepath", st.session_state[SPEC_FILE])
    new_code_filepath = st.text_input("Generators Code filepath", st.session_state[CODE_FILE])
    
    if new_spec_filepath != st.session_state[SPEC_FILE]:
        st.session_state[SPEC_FILE] = new_spec_filepath
    if new_code_filepath != st.session_state[CODE_FILE]:
        st.session_state[CODE_FILE] = new_code_filepath
        
    # TODO: Add resest

    # Load generators
    generators = st.session_state[GENERATORS]

    try:
        with open(new_spec_filepath) as input:
            generators_file = input.read()
            generators_json = load_json(new_spec_filepath)
            new_generators = (generators_from_json(generators_json))
            if generators != new_generators:
                st.session_state[GENERATORS] = new_generators

    except FileNotFoundError:
        st.error('File not found.')
    with st.expander("Raw Generators JSON"):
        st.text(generators_file)

    st.markdown("Images by Freepik from [Flaticon](https://www.flaticon.com/)")