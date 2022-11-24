import streamlit as st
from file_utils import load_json, load_string
from models.generator import Generator, generators_from_json

def config_tab(default_filepath: str, callback) -> list[Generator]:
    global generators
    global spec_filepath
    global code_filepath
    st.write("Configuration Options")
    spec_filepath = st.text_input("Generators Spec filepath", default_filepath)
    code_filepath = st.text_input("Generators Code filepath", "mock_generators/generators")
    try:
        with open(spec_filepath) as input:
            generators_file = input.read()
            generators_json = load_json(spec_filepath)
            callback(generators_from_json(generators_json))
    except FileNotFoundError:
        st.error('File not found.')
    with st.expander("Raw Generators JSON"):
        st.text(generators_file)