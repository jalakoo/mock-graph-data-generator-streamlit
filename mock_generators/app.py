import streamlit as st
from constants import *
from tabs.ideate_tab import ideate_tab
from tabs.generate_tab import import_tab
from tabs.design_tab import design_tab
from tabs.data_importer import data_importer_tab
from tabs.tutorial import tutorial_tab
from tabs.getting_help import get_help_tab
from tabs.dashboard import dashboard_tab

from config import setup_logging, preload_state, load_generators_to_streamlit

# SETUP
st.set_page_config(layout="wide")
setup_logging()
preload_state()
load_generators_to_streamlit()

# UI
# st.title("Mock Graph Data Generator")
# st.markdown("This is a collection of tools to generate mock graph data for [Neo4j](https://neo4j.com) graph databases. NOTE: Chromium browser recommended for best experience.")


generators = None
imported_file = None

# Streamlit runs from top-to-bottom from tabs 1 through 8. This is essentially one giant single page app.  Earlier attempt to use Streamlit's multi-page app functionality resulted in an inconsistent state between pages.

t0, t1, t2, t3, t4, t5, t6 = st.tabs([
    #"⓪ Getting Started",
    #"① Ideate",
    "② Design",
    "③ Generate",
    #"④ Import",
    #"⑤ Dashboard",
    #"Ⓘ Info"
])


with t0:
    design_tab()
with t1:
    import_tab()

# with t0:
#     tutorial_tab()
# with t1:
#     ideate_tab()
# with t2:
#     design_tab()
# with t3:
#     import_tab()
# with t4:
#     data_importer_tab()
# with t5:
#     dashboard_tab()
# with t6:
#     get_help_tab()