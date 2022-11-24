import streamlit as st
from file_utils import load_json, load_string
from models.generator import Generator, generators_from_json

def config_tab(filename: str) -> list[Generator]:
    st.write("Configuration Options")
    filename = st.text_input("Generators filepath", filename)
    try:
        with open(filename) as input:
            generators_file = input.read()
            generators_json = load_json(filename)
            generators = generators_from_json(generators_json)
            return generators
    except FileNotFoundError:
        st.error('File not found.')
    with st.expander("Generators JSON"):
        st.text(generators_file)