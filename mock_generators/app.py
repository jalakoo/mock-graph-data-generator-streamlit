import streamlit as st
from constants import *
from tabs.importing_tab import import_tab
from tabs.design_tab import design_tab
# from tabs.integrated_design_tab import integrated_design_tab
from tabs.data_importer import data_importer_tab
from tabs.tutorial import tutorial_tab
from config import load_generators

# TODO: Move this stuff into the config class
# SETUP
st.set_page_config(layout="wide")

# Default state
if ZIPS_PATH not in st.session_state:
    st.session_state[ZIPS_PATH] = DEFAULT_ZIPS_PATH
if GENERATORS not in st.session_state:
    st.session_state[GENERATORS] = None
if SPEC_FILE not in st.session_state:
    st.session_state[SPEC_FILE] = DEFAULT_GENERATORS_SPEC_FILE
if CODE_FILE not in st.session_state:
    st.session_state[CODE_FILE] = DEFAULT_GENERATORS_CODE_PATH
if SAMPLE_ARROWS_FILE not in st.session_state:
    st.session_state[SAMPLE_ARROWS_FILE] = DEFAULT_ARROWS_SAMPLE_PATH
if IMPORTED_FILENAME not in st.session_state:
    st.session_state[IMPORTED_FILENAME] = ""
if IMPORTS_PATH not in st.session_state:
    st.session_state[IMPORTS_PATH] = DEFAULT_IMPORTS_PATH
# TODO: Replace with reference to selected import file
if IMPORTED_FILE not in st.session_state:
    st.session_state[IMPORTED_FILE] = None
if IMPORTED_NODES not in st.session_state:
    st.session_state[IMPORTED_NODES] = []
if IMPORTED_RELATIONSHIPS not in st.session_state:
    st.session_state[IMPORTED_RELATIONSHIPS] = []
if EXPORTS_PATH not in st.session_state:
    st.session_state[EXPORTS_PATH] = DEFAULT_EXPORTS_PATH
if CODE_TEMPLATE_FILE not in st.session_state:
    st.session_state[CODE_TEMPLATE_FILE] = DEFAULT_CODE_TEMPLATES_FILE
if MAPPINGS not in st.session_state:
    st.session_state[MAPPINGS] = None

load_generators()

# UI
st.title("Mock Graph Data Generator")
st.markdown("This is a collection of tools to generate mock graph data for [Neo4j](https://neo4j.com) graph databases. NOTE: Chromium browser recommended for best experience.")



generators = None
imported_file = None

# Streamlit runs from top-to-bottom from tabs 1 through 8. This is essentially one giant single page app.  Earlier attempt to use Streamlit's multi-page app functionality resulted in an inconsistent state between pages.

t0, t1, t2, t5 = st.tabs([
    "⓪ Tutorial",
    "① Design",
    "② Generate",
    "③ Data Importer"
])

with t0:
    tutorial_tab()
with t1:
    design_tab()
with t2:
    import_tab()
with t5:
    data_importer_tab()