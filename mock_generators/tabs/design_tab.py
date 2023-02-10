import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from constants import *

def design_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/abstract.gif")
    with col2:
        st.write(f"Design Data Model.\n\nUse the [arrows.app](https://arrows.app) then download the .json file to the Import tab.")
    st.markdown("--------")

    c1, c2 = st.columns([8,2])
    with c1:
        components.iframe("https://arrows.app", height=1000, scrolling=False)
    with c2:
        st.write("Generators")
        st.markdown("--------")