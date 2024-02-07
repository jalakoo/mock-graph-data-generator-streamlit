import streamlit as st
from ui.instructions_ui import instructions_ui
from ui.generate_ui import generate_ui
from ui.design_ui import arrows_ui, generators_ui
from ui.ideate_ui import ideate_ui
from ui.export_ui import export_ui
from ui.samples_ui import samples_list
import logging

# SETUP
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
logging.getLogger().setLevel(logging.DEBUG)
logging.info(f'App Started')

# Uncomment to start graph_data_generator logging
# start_logging()

# LOAD any env
neo4j_uri = st.secrets.get("NEO4J_URI", None)
if "NEO4J_URI" not in st.session_state:
    st.session_state["NEO4J_URI"] = neo4j_uri
neo4j_user = st.secrets.get("NEO4J_USER", None)
if "NEO4J_USER" not in st.session_state:
    st.session_state["NEO4J_USER"] = neo4j_user
password = st.secrets.get("NEO4J_PASSWORD", None)
if "NEO4J_PASSWORD" not in st.session_state:
    st.session_state["NEO4J_PASSWORD"] = password
open_ai_key = st.secrets.get("OPENAI_API_KEY", None)
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = open_ai_key

# Setup other state info
if "SAMPLE_PROMPT" not in st.session_state:
    st.session_state["SAMPLE_PROMPT"] = None
if "DOWNLOADING" not in st.session_state:
    st.session_state["DOWNLOADING"] = False
if "UPLOADING" not in st.session_state:
    st.session_state["UPLOADING"] = False
if "ARROWS_DICT" not in st.session_state:
    st.session_state["ARROWS_DICT"] = None
if "JSON_CONFIG" not in st.session_state:
    st.session_state["JSON_CONFIG"] = None
if "SAMPLE_IMAGES" not in st.session_state:
    st.session_state["SAMPLE_IMAGES"] = []


# Header
instructions_ui()

# Modify CSS to keep buttons closer together
# st.markdown("""
#             <style>
#                 div[data-testid="column"] {
#                     width: fit-content !important;
#                     flex: unset;
#                 }
#                 div[data-testid="column"] * {
#                     width: fit-content !important;
#                 }
#             </style>
#             """, unsafe_allow_html=True)

# Body
st.markdown("**① DESIGN**")
# design_ui()
with st.expander("GraphGPT"):
    ideate_ui()
with st.expander("Arrows"):
    arrows_ui()

st.markdown("**② GENERATE**")
generate_ui()

export_ui()

# Side bar
with st.sidebar:
    tab1, tab2 = st.tabs(["Generators", "Samples"])
    with tab1:
        generators_ui()
    with tab2:
        samples_list()