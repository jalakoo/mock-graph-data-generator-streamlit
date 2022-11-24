import streamlit as st
from widgets.config import config_tab
from widgets.generators import generators_tab
from widgets.create import create_tab

# SETUP
DEFAULT_GENERATORS_FILE = "mock_generators/generators.json"
filename = DEFAULT_GENERATORS_FILE

# UI
st.title("Mock Graph Data Generators")
st.write("This is a collection of mock data generators for generating mock graph data in a mockgraphdata app")

tab1, tab2, tab3 = st.tabs(["Config", "Generators", "Create"])
with tab1: 
    generators = config_tab(filename)

with tab2:
    generators_tab(generators)

with tab3:
    create_tab(generators)
