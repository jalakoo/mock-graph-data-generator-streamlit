import streamlit as st
from ui.instructions_ui import instructions_ui
from ui.generate_ui import generate_ui
from ui.config_ui import config_ui
from ui.design_ui import arrows_ui, generators_ui
from ui.ideate_ui import ideate_ui
from ui.export_ui import export_ui
import logging
import json
import graph_data_generator as gdg
from neo4j_uploader import upload

# SETUP
st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
logging.getLogger().setLevel(logging.DEBUG)
logging.info(f'App Started')

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
with st.expander("GraphGPT"):
    ideate_ui()


# with st.expander("Arrows"):
#     arrows_ui()


st.markdown("**② GENERATE**")
prior = None
if st.session_state["ARROWS_DICT"] is not None:
    dict = st.session_state.get("ARROWS_DICT", {}).get('graph', None)
    string = json.dumps(dict, indent=4)
    st.session_state["JSON_CONFIG"] = string
if st.button('Load Sample'):
    sample_raw = json.load(open("graph_data_generator_streamlit/samples/minimal.json"))
    prior = json.dumps(sample_raw, indent=4)
    st.session_state["JSON_CONFIG"] = prior

txt = st.text_area("Enter .JSON config below", height=500, help="Click out of the text area to generate the .zip file.", value=st.session_state.JSON_CONFIG)
def get_data(txt: str):
    mapping = gdg.generate_mapping(txt)
    zip = gdg.package(mapping)
    data = gdg.generate_dictionaries(mapping)
    return data

st.markdown("**③ EXPORT**")
if st.button("wtf"):
    data = get_data(txt)
    st.write("wtf")
# if txt is None:
#     st.error("Add JSON config to generate data")
# else:
#     # Generate data
#     mapping = gdg.generate_mapping(txt)
#     zip = gdg.package(mapping)
#     data = gdg.generate_dictionaries(mapping)

#     filename = st.text_input("Name of file", value="mock_data", help="Name of file to be used for the.zip file. Ignored if pushing directly to a Neo4j database instance.")

#     st.download_button(
#         label = "Download .zip file",
#         data = zip,
#         file_name = f"{filename}.zip",
#         mime = "text/plain"
#     )

# # Side bar
# with st.sidebar:
#     generators_ui()