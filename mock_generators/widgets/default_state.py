import streamlit as st
from constants import *
import logging
from models.generator import Generator, generators_from_json
from file_utils import load_json, load_string
from models.mapping import Mapping
import sys

# Setup default session state if not already available

def load_state():
    # logging.info(f'default_state: loading state...')
    if ZIPS_PATH not in st.session_state:
        st.session_state[ZIPS_PATH] = DEFAULT_ZIPS_PATH
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
        st.session_state[MAPPINGS] = Mapping(
            nodes={}, 
            relationships={})
    if GENERATORS not in st.session_state:
        spec_filepath = st.session_state[SPEC_FILE]
        try:
            generators_json = load_json(spec_filepath)
            generators = generators_from_json(generators_json)
            st.session_state[GENERATORS] = generators # This not sticking?
            # Generators will be in a dict
            # logging.info(f'default_state.py: Generators loaded: {generators}')

        except FileNotFoundError:
            st.error('No generator file found.')
            st.session_state[GENERATORS] = None
        except:
            st.error(f'Error loading generators from {spec_filepath}: {sys.exc_info()[0]}')
    # else:
    #     logging.info(f'default_state.py: Generators already loaded: {st.session_state[GENERATORS]}')
    logging.info(f'default_state: loading state complete.')
