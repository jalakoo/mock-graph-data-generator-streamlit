import streamlit as st
from models.generator import GeneratorArg, GeneratorType
import logging

def input_type(label: str, type: GeneratorType, key:str) -> any:
    if type == GeneratorType.STRING:
        return st.text_input(label, key=key)
    elif type == GeneratorType.INT or type == GeneratorType.FLOAT:
        return st.number_input(label, key=key)
    elif type == GeneratorType.BOOL:
        return st.checkbox(label, key=key)
    elif type == GeneratorType.DATETIME:
        date = st.date_input(label, key=key)
        return date.isoformat()
    else:
        raise Exception("Unknown type: " + type)

def add_arg(number, callback) -> dict:
    st.write(f"Argument {number + 1}")
    type_input= st.radio("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"arg_type_{number}_type_input")
    # type_input = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key = f"arg_type_{number}_type_input")
    type = GeneratorType.typeFromString(type_input.lower())
    label = st.text_input("Name", key = f"arg_type_{number}_label")
    default = input_type("Default Value", type, key=f"arg_type_{number}_default")
    logging.info(f'add_arg: {type_input}, {type}, {label}, {default}')
    if st.button("Cancel", key=f"arg_type_{number}_cancel"):
        callback(None)
    if st.button("Save", key=f'arg_type_{number}_save'):
        callback({
            "type": type,
            "label": label,
            "default": default
        })

