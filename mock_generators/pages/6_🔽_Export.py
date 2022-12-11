import streamlit as st
from streamlit_extras.colored_header import colored_header
from widgets.header import header
from constants import *
from widgets.default_state import load_state
from widgets.folder_files import folder_files_expander

# SETUP
# page icon here not being respected
st.set_page_config(
    layout="wide",
    page_title="Export"
)
load_state()
export_folder = st.session_state[EXPORTS_PATH]
zips_folder = st.session_state[ZIPS_PATH]

# UI
header(
    title=EXPORT_PAGE_TITLE,
    description=f"Review and download generated data for upload to [Neo4j Aura Console](https://console.neo4j.io)",
    color_name="Green",
    prior_page="Generate"
)

ec1, ec2 = st.tabs(["Generated Downloads", "Most Recently Generated Files"])

with ec2:
    folder_files_expander(export_folder, widget_id="export_tab")

with ec1:
    folder_files_expander(zips_folder, widget_id="export_tab", enable_download=True, enable_delete_button=True)

# with ec3:
#     st.write(f"Upload desired .zip file to Neo4j:")
#     link = '[Neo4j Aura Console](https://console.neo4j.io)'
#     st.markdown(link, unsafe_allow_html=True)