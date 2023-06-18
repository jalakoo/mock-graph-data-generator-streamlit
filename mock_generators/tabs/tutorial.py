from streamlit_player import st_player
import streamlit as st

def tutorial_tab():
    st.title("Mock Graph Data Generator")
    st.markdown(
        """
        This app is a central collection of existing tools for generating  interconnected mock data that can also be imported directly into a [Neo4j](https://neo4j.com) graph database.

        Move along each tab from left to right to define the model (or schema), generate the mock data, then optionally import and query the data. Instructions are available within each tab and a general walkthrough video is available below.
        
        NOTES: 
        - Chromium browser recommended for best experience.
        - Each tool may require independent logins with first use.
    """)
    url = st.secrets["VIDEO_TUTORIAL_URL"]
    st_player(url, height=600)