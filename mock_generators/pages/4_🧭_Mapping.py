import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Mappings"
)

header(
    title=MAPPINGS_PAGE_TITLE,
    description=f"Map relationships and count generators to determine number of nodes and relationships to create.",
    color_name="Yellow",
    prior_page="Properties",
    next_page="Generate"
)