import streamlit as st
from models.generator import GeneratorArg, GeneratorType
import logging

def input_type(label: str, type: str, key:str) -> any:
    type = type.lower()
    if type == "string":
        return st.text_input(label, key=key)
    elif type == "int":
        return st.number_input(label, key=key, value = 0)
    elif type == "float":
        return st.number_input(label, key=key, value = 0.0)
    elif type == "bool":
        return st.checkbox(label, key=key)
    elif type == "datetime":
        date = st.date_input(label, key=key)
        return date.isoformat()
    else:
        raise Exception("Unknown type: " + type)

def argument_widget(index, callback) -> dict:
    st.write(f"Argument {index + 1}")
    type_input= st.radio("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"arg_type_{index}_type_input")
    # type_input = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key = f"arg_type_{index}_type_input")
    # type = GeneratorType.typeFromString(type_input.lower())
    label = st.text_input("Name", key = f"arg_type_{index}_label")
    default = input_type("Default Value", type_input, key=f"arg_type_{index}_default")
    logging.info(f'add_arg: {type_input}, {type}, {label}, {default}')
    # if st.button("Cancel", key=f"arg_type_{index}_cancel"):
    #     callback(index, None)
    # if st.button("Save", key=f'arg_type_{index}_save'):
    callback(index, {
        "type": type_input.lower(),
        "label": label,
        "default": default
    })

