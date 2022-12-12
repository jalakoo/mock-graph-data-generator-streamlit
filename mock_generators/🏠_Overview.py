import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *
from models.generator import Generator
from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.property_mapping import PropertyMapping
from widgets.default_state import load_state

# Default state
# if ZIPS_PATH not in st.session_state:
#     st.session_state[ZIPS_PATH] = DEFAULT_ZIPS_PATH
# if GENERATORS not in st.session_state:
#     st.session_state[GENERATORS] = None
# if SPEC_FILE not in st.session_state:
#     st.session_state[SPEC_FILE] = DEFAULT_GENERATORS_SPEC_FILE
# if CODE_FILE not in st.session_state:
#     st.session_state[CODE_FILE] = DEFAULT_GENERATORS_CODE_PATH
# if SAMPLE_ARROWS_FILE not in st.session_state:
#     st.session_state[SAMPLE_ARROWS_FILE] = DEFAULT_ARROWS_SAMPLE_PATH
# if IMPORTED_FILENAME not in st.session_state:
#     st.session_state[IMPORTED_FILENAME] = ""
# if IMPORTS_PATH not in st.session_state:
#     st.session_state[IMPORTS_PATH] = DEFAULT_IMPORTS_PATH
# # TODO: Replace with reference to selected import file
# if IMPORTED_FILE not in st.session_state:
#     st.session_state[IMPORTED_FILE] = None
# if IMPORTED_NODES not in st.session_state:
#     st.session_state[IMPORTED_NODES] = []
# if IMPORTED_RELATIONSHIPS not in st.session_state:
#     st.session_state[IMPORTED_RELATIONSHIPS] = []
# if EXPORTS_PATH not in st.session_state:
#     st.session_state[EXPORTS_PATH] = DEFAULT_EXPORTS_PATH
# if CODE_TEMPLATE_FILE not in st.session_state:
#     st.session_state[CODE_TEMPLATE_FILE] = DEFAULT_CODE_TEMPLATES_FILE
# if MAPPINGS not in st.session_state:
#     st.session_state[MAPPINGS] = Mapping(
#         nodes={}, 
#         relationships={})

load_state()

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Overview",
    page_icon="🏠",
)

header(
    title=OVERVIEW_PAGE_TITLE,
    description=f'Welcome to the Mock Graph Data Generator. This is a collection of tools to generate mock graph data for [Neo4j](https://neo4j.com) graph databases.',
    color_name="red",
    next_page="Design"
)



