import streamlit as st
from constants import *
from file_utils import load_json, load_string
from models.generator import Generator, generators_from_json
import os
import sys
import logging
from widgets.folder_files import folder_files_expander

def load_generators():

    spec_filepath = st.session_state[SPEC_FILE]
    generators = st.session_state[GENERATORS]
    try:
        with open(spec_filepath) as input:
            # generators_file = input.read()
            generators_json = load_json(spec_filepath)
            new_generators = generators_from_json(generators_json)
            if generators != new_generators:
                st.session_state[GENERATORS] = new_generators

    except FileNotFoundError:
        st.error('File not found.')