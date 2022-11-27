import streamlit as st
from constants import *
from file_utils import load_json, load_string
from models.generator import Generator, generators_from_json
import os

def config_tab() -> list[Generator]:

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/options.gif")
    with col2:
        st.write("Optionally change the export path, source locations for importing and reading generator specifications and code files. Generators are code functions used to generate specific types of mock data (ie: email generator for creating mock email addresses).")
    st.markdown("--------")


    # Load generators
    gc1, gc2 = st.columns([1,2])
    with gc1:
        new_spec_filepath = st.text_input("Generators Spec filepath", st.session_state[SPEC_FILE])
        if new_spec_filepath != st.session_state[SPEC_FILE]:
            st.session_state[SPEC_FILE] = new_spec_filepath
    with gc2:
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
        st.write("Loaded spec file")
        with st.expander("Generators Spec JSON"):
            st.code(generators_file)

    # Load generators code
    cc1, cc2 = st.columns([1,2])
    with cc1:
        new_code_filepath = st.text_input("Generators Code filepath", st.session_state[CODE_FILE])
        if new_code_filepath != st.session_state[CODE_FILE]:
            st.session_state[CODE_FILE] = new_code_filepath
    files = ""
    with cc2:
        try:
            for root, dirs, files in os.walk(st.session_state[CODE_FILE]):
                for file in files:
                    if file.endswith(".py"):
                        files += file
        except:
            st.error('Could not retrieve generator .py files from specified code filepath.')
        st.write("Loaded code files")
        with st.expander("Generators Code Files"):
            if files == "":
                st.warning("No files found in specified path.")
            # TODO: Make files list vertically
            st.code(files)

    # Load new generator template file
    cc1, cc2 = st.columns([1,2])
    with cc1:
        new_template_filepath = st.text_input("Generator Code Template file", st.session_state[CODE_TEMPLATE_FILE])
        if new_template_filepath != st.session_state[CODE_TEMPLATE_FILE]:
            st.session_state[CODE_TEMPLATE_FILE] = new_template_filepath
        with open(st.session_state[CODE_TEMPLATE_FILE], "r") as file:
            code_template = file.read()
    with cc2:
        st.write("Loaded code template file")
        with st.expander("Generator Code Template"):
            st.code(code_template)

    # Load export path
    new_exports_filepath = st.text_input("Generated Data filepath", st.session_state[EXPORTS_PATH])
    if new_exports_filepath != st.session_state[EXPORTS_PATH]:
        st.session_state[EXPORTS_PATH] = new_exports_filepath
    
    # TODO: Verify export path is available

    # TODO: Add resest




    st.markdown("Images by Freepik from [Flaticon](https://www.flaticon.com/)")