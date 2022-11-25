import streamlit as st
from constants import *
from widgets.config import config_tab
from widgets.generators import generators_tab
from widgets.create import create_tab
from widgets.mapping import mapping_tab
from widgets.export import export_tab
from widgets.importing import import_tab
from models.generator import Generator


# UI
st.title("Mock Graph Data Generators")
st.write("This is a collection of mock data generators for generating mock graph data in a mockgraphdata app")

generators = None
imported_file = None

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Config >", "Import >",  "Mapping >", "Generators >", "New Generator >", "Export"])

with tab1:
    config_tab()

with tab2:
    import_tab()

with tab3:
    mapping_tab()

with tab4:
    generators_tab()

with tab5:
    create_tab()

with tab6:
    export_tab()