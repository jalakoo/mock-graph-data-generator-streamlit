import streamlit as st
import hydralit_components as hc
from constants import *
from streamlit_extras.switch_page_button import switch_page


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

    if menu_id != st.session_state.PRIOR_PAGE:
        st.session_state.PRIOR_PAGE = menu_id
        switch_page(menu_id.lower())



