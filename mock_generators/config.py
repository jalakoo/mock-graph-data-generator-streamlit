import streamlit as st
from constants import *
from file_utils import load_json
from models.generator import generators_from_json

def preload_state():
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

def load_generators():
    spec_filepath = st.session_state[SPEC_FILE]
    generators = st.session_state[GENERATORS]
    try:
        with open(spec_filepath) as input:
            generators_json = load_json(spec_filepath)
            new_generators = generators_from_json(generators_json)
            if generators != new_generators:
                st.session_state[GENERATORS] = new_generators

    except FileNotFoundError:
        st.error('File not found.')