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
from widgets.nav_bar import nav_bar

# Default state
load_state()

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Overview",
    page_icon="🏠",
)

# UI
# nav_bar()

header(
    title=OVERVIEW_PAGE_TITLE,
    description=f'Welcome to the Mock Graph Data Generator. This is a collection of tools to generate mock graph data for [Neo4j](https://neo4j.com) graph databases.',
    color_name="red",
    next_page="Design"
)



