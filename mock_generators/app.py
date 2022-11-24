import streamlit as st
from widgets.config import config_tab
from widgets.generators import generators_tab
from widgets.create import create_tab
from models.generator import Generator

# SETUP
DEFAULT_GENERATORS_SPEC_FILE = "mock_generators/generators.json"
DEFAULT_GENERATORS_CODE_PATH = "mock_generators/generators"
spec_filepath = DEFAULT_GENERATORS_SPEC_FILE
code_filepath = DEFAULT_GENERATORS_CODE_PATH

# UI
st.title("Mock Graph Data Generators")
st.write("This is a collection of mock data generators for generating mock graph data in a mockgraphdata app")

generators = None
tab1, tab2, tab3 = st.tabs(["Config", "Generators", "Create"])

with tab1:
    def callback(new_generators:list[Generator]):
        global generators
        generators = new_generators

    config_tab(
        spec_filepath, 
        code_filepath, 
        callback)

with tab2:
    generators_tab(
        generators, 
        code_filepath)

with tab3:
    create_tab(
        generators = generators,
        spec_filepath = spec_filepath,
        code_filepath= code_filepath)
