import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *

# SETUP
# header(
#     title=DESIGN_PAGE_TITLE,
#     description=f'Use the free [arrows.app](https://arrows.app) to design the data model for your mock graph data. When completed, click on the "Download/Export" button to download a .json file to upload in　the "Import" page.',
#     color_name="DarkOrange",
#     prior_page="Overview",
#     next_page="Import"
# )


def design_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/abstract.gif")
    with col2:
        st.write(f"Design Data Model.\n\nUse the [arrows.app](https://arrows.app) then download the .json file to the Import tab.")
    st.markdown("--------")

    components.iframe("https://arrows.app", height=1000, scrolling=False)