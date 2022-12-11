import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *
from widgets.node_row import nodes_row
from widgets.relationship_row import relationship_row
from widgets.property_row import property_row
from widgets.default_state import load_state
import json
from models.mapping import Mapping
from file_utils import load_json
from models.generator import Generator, generators_from_json
import logging
from streamlit_toggle import st_toggle_switch

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Properties"
)
load_state()
nodes = st.session_state[IMPORTED_NODES]
relationships = st.session_state[IMPORTED_RELATIONSHIPS]
current_file = st.session_state[IMPORTED_FILE]
generators = st.session_state[GENERATORS]
all_global_properties = None

if current_file is not None:
    try:
        json_file = json.loads(current_file)
        nodes = json_file["nodes"]
        relationships = json_file["relationships"]
        if nodes is None:
            nodes = []
        if relationships is None:
            relationships = []
        
    except json.decoder.JSONDecodeError:
        st.error('JSON file is not valid.')

# UI
header(
    title=PROPERTIES_PAGE_TITLE,
    description=f"Set node and relationship property data generators.",
    color_name="Gold",
    prior_page="Import",
    next_page="Mapping"
)

filename = st.session_state[IMPORTED_FILENAME]
if filename is None or filename == "":
    st.write(f'No import file currently loaded. Go to the [Import](Import) page to load a file.')
else:
    st.write(f"Current import file: {filename}")

tab1, tab2, tab3 = st.tabs(["Globals", "Nodes", "Relationships"])
with tab1:
    # include_globals = st.checkbox("Include Global Properties", value=False, help="Include global properties in data generation. These will overwrite any node or relationship local properties of the same name.")
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
    should_expand = False
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
with tab2:
    num_nodes = st.number_input("Number:", min_value=0, value=len(nodes), key="mapping_number_of_nodes", help="Adjust the number of nodes to generate data for")
    for i in range(num_nodes):
        if i < len(nodes):
            nodes_row(
                nodes[i], 
                generators=generators,
                should_start_expanded=should_expand,
                additional_properties=all_global_properties)
        else:
            nodes_row(None)

with tab3:
    # TODO: Add ability to add ALL RELATIONSHIPS ONLY properties
    num_relationships = st.number_input("Number:", min_value=0, value=len(relationships), key="mapping_number_of_relationships", help="Adjust the number of relationships to generate data for")
    for i in range(num_relationships):
        if i < len(relationships):
            relationship_row(
                relationships[i],
                should_start_expanded=should_expand,
                additional_properties=all_global_properties)
        else:
            relationship_row(None)