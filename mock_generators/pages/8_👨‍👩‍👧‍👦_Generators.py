import streamlit as st
from tabs.generators_tab import generators_tab
from tabs.new_generator_tab import create_tab
from widgets.header import header
from constants import *

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Generators"
)

st.subheader(GENERATORS_PAGE_TITLE)
st.write(
    f'<hr style="background-color: grey; margin-top: 0;'
    ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
    unsafe_allow_html=True,
)
st.caption(f"Optional Configuration Options.\n\nChange the export path, source locations for importing and reading generator specifications and code files. Generators are code functions used to generate specific types of mock data (ie: email generator for creating mock email addresses).")

tab1, tab2 = st.tabs(["Search Generators", "New Generator"])

with tab1:
    generators_tab()
with tab2:
    create_tab()