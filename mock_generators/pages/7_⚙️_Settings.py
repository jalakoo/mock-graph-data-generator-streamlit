import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *


# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Settings"
)

st.subheader(SETTINGS_PAGE_TITLE)
st.write(
    f'<hr style="background-color: grey; margin-top: 0;'
    ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
    unsafe_allow_html=True,
)
st.caption(f"Optional Configuration Options.\n\nChange the export path, source locations for importing and reading generator specifications and code files. Generators are code functions used to generate specific types of mock data (ie: email generator for creating mock email addresses).")