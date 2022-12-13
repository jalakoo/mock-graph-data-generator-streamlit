import streamlit as st
import hydralit_components as hc
from constants import *
from streamlit_extras.switch_page_button import switch_page

from tabs.config_tab import config_tab
from tabs.design_tab import design_tab
from tabs.generators_tab import generators_tab
from tabs.new_generator_tab import create_tab
from tabs.mapping_tab import mapping_tab
from tabs.generate_tab import generate_tab
from tabs.export_tab import export_tab
from tabs.importing_tab import import_tab

def nav_bar():
    # SETUP
    if "PRIOR_PAGE" not in st.session_state:
        st.session_state.PRIOR_PAGE = OVERVIEW_SHORT_TITLE

    menu_data = [
        {'label': DESIGN_SHORT_TITLE},
        {'label': IMPORT_SHORT_TITLE},
        {'label': PROPERTIES_SHORT_TITLE},
        {'label': MAPPINGS_SHORT_TITLE},
        {'label': GENERATE_SHORT_TITLE},
        {'label': EXPORT_SHORT_TITLE},
        {'label': SETTINGS_SHORT_TITLE},
        {'label': GENERATORS_SHORT_TITLE}
    ]
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        home_name="Overview",
        hide_streamlit_markers=False,
        sticky_mode='pinned'
    )

    # if menu_id != st.session_state.PRIOR_PAGE:
    #     st.session_state.PRIOR_PAGE = menu_id
    #     switch_page(menu_id.lower())

    if menu_id == DESIGN_SHORT_TITLE:
        design_tab()
    
    


