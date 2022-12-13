import streamlit as st
from widgets.header import header
from constants import *
from widgets.node_row import nodes_row
from widgets.relationship_row import relationship_row
from widgets.property_row import property_row
from widgets.default_state import load_state
import json
from streamlit_toggle import st_toggle_switch
import logging

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Properties"
)
# State Info
load_state()
node_dicts = st.session_state[IMPORTED_NODES]
relationship_dicts = st.session_state[IMPORTED_RELATIONSHIPS]
generators = st.session_state[GENERATORS]
filename = st.session_state[IMPORTED_FILENAME]
# current_file = st.session_state[IMPORTED_FILE]
# if current_file is not None:
#     try:
#         json_file = json.loads(current_file)
#         # Bring in the raw import data for nodes and relationships
#         node_dicts = json_file["nodes"]
#         relationship_dicts = json_file["relationships"]
#         if node_dicts is None:
#             node_dicts = []
#         if relationship_dicts is None:
#             relationship_dicts = []
        
#     except json.decoder.JSONDecodeError:
#         st.error('JSON file is not valid.')

if generators is None:
    logging.error(f"properties page: Generators not loaded")

# Page Info
all_global_properties = None

# UI
header(
    title=PROPERTIES_PAGE_TITLE,
    description=f"Set node and relationship property data generators.",
    color_name="Gold",
    prior_page="Import",
    next_page="Mapping"
)

# Display Current imported filename
if filename is None or filename == "":
    st.write(f'No import file currently loaded. Go to the [Import](Import) page to load a file.')
else:
    st.write(f"Current import file: {filename}")

# Segment major sections
tab1, tab2, tab3 = st.tabs(["Globals", "Nodes", "Relationships"])

# Global Property options
with tab1:
    tab1g, tab2g = st.columns([5,1])
    with tab1g:
        st.write(f'Properties that can be add to ALL nodes and relationships.')
    with tab2g:
        include_globals = st_toggle_switch(
            label="Enable",
            key="enable_global_properties",
            default_value=False,
            label_after=False,
            inactive_color="#808080",  # optional
            active_color="#00FF00",  # optional
            track_color="#008000",  # optional
        )
    if include_globals == True:
        num_global_properties = st.number_input("Number of Global Properties", min_value=0, value=0)
        all_global_properties = []
        if include_globals == True:
            for i in range(num_global_properties):
                global_property = property_row(
                    type="global",
                    id = f'',
                    index = i,
                    properties = []
                )
                all_global_properties.append(global_property)

# Node Property options
with tab2:
    num_nodes = st.number_input("Number:", min_value=0, value=len(node_dicts), key="mapping_number_of_nodes", help="Adjust the number of nodes to generate data for")
    for i in range(num_nodes):
        if i < len(node_dicts):
            nodes_row(
                node_dicts[i], 
                generators=generators,
                should_start_expanded=False,
                additional_properties=all_global_properties)
        else:
            nodes_row(None)

# Relationship Property options
with tab3:
    # TODO: Add ability to add ALL RELATIONSHIPS ONLY properties
    num_relationships = st.number_input("Number:", min_value=0, value=len(relationship_dicts), key="mapping_number_of_relationships", help="Adjust the number of relationships to generate data for")
    for i in range(num_relationships):
        if i < len(relationship_dicts):
            relationship_row(
                relationship_dicts[i],
                should_start_expanded=False,
                generators=generators,
                additional_properties=all_global_properties)
        else:
            relationship_row(None)