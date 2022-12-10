import streamlit as st
from constants import *
from models.generator import GeneratorArg, GeneratorType
import logging

def input_type(label: str, type: str, key:str) -> any:
    type = type.lower()
    help = "An optional default value for the argument that will populate this generator arg when the generator is selected."
    if type == "string":
        return st.text_input(label, key=key, help=help)
    elif type == "int":
        return st.number_input(label, key=key, value = 0, help=help)
    elif type == "float":
        return st.number_input(label, key=key, value = 0.0, help=help)
    elif type == "bool":
        return st.checkbox(label, key=key, help=help)
    elif type == "datetime":
        date = st.date_input(label, key=key, help=help)
        return date.isoformat()
    else:
        raise Exception("Unknown type: " + type)

def argument_widget(
    index: int,
    type: str
    ) -> dict:
    # For new generator arguments
    st.write(f"Optional Argument {index + 1}")
    type_input= st.radio("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"arg_type_{index}_type_input")

    label = st.text_input("Name", key = f"arg_type_{index}_label", help="Name of the argument that will be displayed in the UI. (e.g. 'Name' or 'Age'. Leave blank to skip this argument.")

    default = input_type("Default Value", type_input, key=f"arg_type_{index}_default")
    # logging.info(f'add_arg: {type_input}, {type}, {label}, {default}')

    if label is not None and label != "":
        return {
            "type": type_input.lower(),
            "label": label,
            "default": default
        }
    return None
