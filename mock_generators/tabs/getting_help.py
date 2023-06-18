import streamlit as st

def get_help_tab():
    version = st.secrets["VERSION"]
    st.write(f"Version {version}")
    st.markdown("""
    Post issues and comments in this [github repo](https://github.com/jalakoo/mock-graph-data-generator/issues)
    """)