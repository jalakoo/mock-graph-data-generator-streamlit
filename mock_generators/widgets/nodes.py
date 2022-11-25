import streamlit as st
from constants import *

def nodes_row(
    node: dict
    ):
    id = node.get("id")
    labels = node.get("labels")
    labels.append(node.get("caption"))
    with st.expander(f"Node id: {id}, labels: {labels}"):
        properties = node.get("properties")
        st.write('Property assignments')
        for key,value in properties.items():
            st.write(f"{key}: {value}")
