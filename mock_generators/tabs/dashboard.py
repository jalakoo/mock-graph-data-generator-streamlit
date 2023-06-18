import streamlit as st
import streamlit.components.v1 as components

def dashboard_tab():
    st.markdown("""
    Use Neodash below to create a simple data dashboard from a Neo4j database. Requires knowledge of [Cypher](https://neo4j.com/docs/getting-started/cypher-intro/)
    """)
    # Neodash interface
    components.iframe("https://neodash.graphapp.io", height=1000, scrolling=True)