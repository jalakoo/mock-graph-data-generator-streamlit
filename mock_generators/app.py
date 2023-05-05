import streamlit as st
from constants import *
from tabs.importing_tab import import_tab
from tabs.design_tab import design_tab
from tabs.data_importer import data_importer_tab
from tabs.tutorial import tutorial_tab
from config import preload_state, load_generators_to_streamlit

# SETUP
st.set_page_config(layout="wide")
preload_state()
load_generators_to_streamlit()

# UI
st.title("Mock Graph Data Generator")
st.markdown("This is a collection of tools to generate mock graph data for [Neo4j](https://neo4j.com) graph databases. NOTE: Chromium browser recommended for best experience.")


generators = None
imported_file = None

# Streamlit runs from top-to-bottom from tabs 1 through 8. This is essentially one giant single page app.  Earlier attempt to use Streamlit's multi-page app functionality resulted in an inconsistent state between pages.

t0, t1, t2, t5 = st.tabs([
    "⓪ Tutorial",
    "① Design",
    "② Generate",
    "③ Data Importer"
])

with t0:
    tutorial_tab()
with t1:
    design_tab()
with t2:
    import_tab()
with t5:
    data_importer_tab()