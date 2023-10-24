import streamlit as st
from ui.instructions_ui import instructions_ui
from ui.generate_ui import generate_ui
from ui.config_ui import config_ui
from ui.design_ui import arrows_ui, generators_ui
from ui.ideate_ui import ideate_ui
import logging

# SETUP
st.set_page_config(layout="wide")
logging.getLogger().setLevel(logging.DEBUG)
logging.info(f'App Started')

# Header
instructions_ui()


# Body
c1, c2 = st.columns([8,2])
with c1:
    st.markdown("**① DESIGN**")
    with st.expander("GraphGPT"):
        ideate_ui()
    with st.expander("Arrows Data Modeler"):
        arrows_ui()

    st.markdown("**② GENERATE**")
    generate_ui()
with c2:
    generators_ui()