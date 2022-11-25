import streamlit as st
from constants import *
from file_utils import load_json, load_string
from models.generator import Generator, generators_from_json

def config_tab() -> list[Generator]:
    default_spec_filepath = st.session_state[SPEC_FILE]
    default_code_filepath = st.session_state[CODE_FILE]

    st.write("This is where you can change the source locations for importing and reading generator specifications and code files.")
    st.markdown("--------")

    new_spec_filepath = st.text_input("Generators Spec filepath", default_spec_filepath)
    new_code_filepath = st.text_input("Generators Code filepath", default_code_filepath)

    # Update filepaths
    if new_spec_filepath != default_spec_filepath:
        st.session_state[SPEC_FILE] = new_spec_filepath
    if new_code_filepath != default_code_filepath:
        st.session_state[CODE_FILE] = new_code_filepath

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