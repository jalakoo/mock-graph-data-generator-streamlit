from streamlit_player import st_player
import streamlit as st

def instructions_ui():
    st.title("Graph Data Generator App")
    st.markdown(
        """
        This app is a central collection tools built around the [graph-data-generator](https://pypi.org/project/graph-data-generator/) package for generating .csvs of interconnected mock data that can be imported into databases, including a [Neo4j](https://neo4j.com) graph database.
        
        NOTES: 
        - Chromium browser recommended for best experience.
        - Each tool may require independent logins with first use.
    """)
    # url = st.secrets["VIDEO_TUTORIAL_URL"]
    # st_player(url, height=600)