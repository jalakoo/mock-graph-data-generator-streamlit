import streamlit as st


def config_ui():

    # Display current app version
    # TODO: Pull this directly from the pyproject.toml
    version = "0.7.10"
    st.write(f"Version {version}")
