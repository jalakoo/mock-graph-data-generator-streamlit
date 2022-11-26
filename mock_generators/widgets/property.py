import streamlit as st
from constants import *
import logging
from models.generator import GeneratorArg, GeneratorType

def property_row(key: str, type: str):
    st.write(f"{key}: {type}")