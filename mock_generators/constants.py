import streamlit as st

# Default local filepaths
DEFAULT_GENERATORS_SPEC_FILE = "mock_generators/generators.json"
DEFAULT_GENERATORS_CODE_PATH = "mock_generators/generators"
DEFAULT_ARROWS_SAMPLE_PATH = "mock_generators/samples/arrows.json"


# Streamlit session keys
GENERATORS = "generators"
SPEC_FILE = "spec_filepath"
CODE_FILE = "code_filepath"
IMPORTED_FILE = "uploaded_file"
SAMPLE_ARROWS_FILE= "sample_arrows"
NEW_ARGS = "new_args"


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
