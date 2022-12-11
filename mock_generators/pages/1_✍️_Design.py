import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *

# SETUP
st.set_page_config(
    layout="wide",
    page_title="Design"
)

header(
    title=DESIGN_PAGE_TITLE,
    description=f'Use the free [arrows.app](https://arrows.app) to design the data model for your mock graph data. When completed, click on the "Download/Export" button to download a .json file to upload in　the "Import" page.',
    color_name="DarkOrange",
    prior_page="Overview",
    next_page="Import"
)

components.iframe("https://arrows.app", height=1000, scrolling=False)