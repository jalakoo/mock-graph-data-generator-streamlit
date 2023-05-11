from streamlit_player import st_player
import streamlit as st

def tutorial_tab():
    url = st.secrets["VIDEO_TUTORIAL_URL"]
    st_player(url, height=600)