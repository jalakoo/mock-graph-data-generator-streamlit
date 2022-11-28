import streamlit as st
from constants import *
from tabs.config import config_tab
from tabs.generators import generators_tab
from tabs.create import create_tab
from tabs.mapping import mapping_tab
from tabs.generate import generate_tab
from tabs.export import export_tab
from tabs.importing import import_tab
from models.generator import Generator
from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping

# SETUP
st.set_page_config(layout="wide")

# Default state
if GENERATORS not in st.session_state:
    st.session_state[GENERATORS] = None
if SPEC_FILE not in st.session_state:
    st.session_state[SPEC_FILE] = DEFAULT_GENERATORS_SPEC_FILE
if CODE_FILE not in st.session_state:
    st.session_state[CODE_FILE] = DEFAULT_GENERATORS_CODE_PATH
if SAMPLE_ARROWS_FILE not in st.session_state:
    st.session_state[SAMPLE_ARROWS_FILE] = DEFAULT_ARROWS_SAMPLE_PATH
if IMPORTED_FILE not in st.session_state:
    st.session_state[IMPORTED_FILE] = None
if NEW_ARGS not in st.session_state:
    st.session_state[NEW_ARGS] = []
if EXPORTS_PATH not in st.session_state:
    st.session_state[EXPORTS_PATH] = DEFAULT_EXPORTS_PATH
if CODE_TEMPLATE_FILE not in st.session_state:
    st.session_state[CODE_TEMPLATE_FILE] = DEFAULT_CODE_TEMPLATES_FILE
if MAPPINGS not in st.session_state:
    st.session_state[MAPPINGS] = Mapping(
        nodes={}, 
        relationships={})

# UI
st.title("Mock Graph Data Generator")
st.markdown("This is a collection of tools to generate mock graph data for [Neo4j](https://neo4j.com) graph databases.")

generators = None
imported_file = None

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Config >", "Import >",  "Mapping >", "Generators >", "New Generator >", "Generate >", "Export"])

with tab1:
    config_tab()

with tab2:
    import_tab()

with tab3:
    mapping_tab()

with tab4:
    generators_tab()

with tab5:
    create_tab()

with tab6:
    generate_tab()

with tab7:
    export_tab()