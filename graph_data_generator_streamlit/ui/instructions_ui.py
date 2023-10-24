from streamlit_player import st_player
import streamlit as st

def instructions_ui():
    st.title("Graph Data Generator App")
    st.markdown(
        """
        This app is a central collection tools built around the [graph-data-generator](https://pypi.org/project/graph-data-generator/) package for generating interconnected mock data. 
        
        Chromium browser recommended for best experience.
    """)
    # url = st.secrets["VIDEO_TUTORIAL_URL"]
    # st_player(url, height=600)