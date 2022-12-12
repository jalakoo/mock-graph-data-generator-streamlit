import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *
from models.mapping import Mapping
from widgets.default_state import load_state
from widgets.node_mapping_row import node_mapping_row
from widgets.relationship_mapping_row import relationship_mapping_row

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Mappings"
)

load_state()
mapping = st.session_state[MAPPINGS]
if mapping is None or mapping == Mapping.empty():
    st.error(f'No mapping found. Please import from the "Import" page or finalize property options in the "Properties" page.')
    st.stop()
node_mappings = mapping.nodes
relationship_mappings = mapping.relationships
generators = st.session_state[GENERATORS]
if generators is None or len(generators) == 0:
    st.error(f'No generators found')
    st.stop()
filename = st.session_state[IMPORTED_FILENAME]
current_file = st.session_state[IMPORTED_FILE]

# UI
header(
    title=MAPPINGS_PAGE_TITLE,
    description=f"Map relationships and count generators to determine number of nodes and relationships to create.",
    color_name="Yellow",
    prior_page="Properties",
    next_page="Generate"
)

# This page similar to properties page as it's features are pulled from the original design

# Segment major sections
tab1, tab2 = st.tabs(["Nodes", "Relationships"])

# Node Property options
with tab1:
    for node in node_mappings.values():
        node_mapping_row(
            node, 
            generators=generators,
            should_start_expanded=False)

# Relationship Property options
with tab2:
    for relationship in relationship_mappings.values():
        relationship_mapping_row(
            relationship,
            should_start_expanded=False,
            generators=generators)


