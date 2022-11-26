import streamlit as st
from constants import *

def relationship_row(relationship: dict):
    id = relationship.get("id")
    type = relationship.get("type")
    fromId = relationship.get("fromId")
    toId = relationship.get("toId")
    with st.expander(f"relationship id: {id}, type: {type}, from: {fromId}, to: {toId}"):
        properties = relationship.get("properties")
        st.write('Property assignments')
        for key,value in properties.items():
            st.write(f"{key}: {value}")