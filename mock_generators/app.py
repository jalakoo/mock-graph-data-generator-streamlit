import argparse
import logging
import streamlit as st
from file_utils import load_json, load_string
from template_selector import generic_template
from new_generator import createGenerator
from models.generator import Generator, GeneratorType, generators_from_json
import random
import importlib
from widgets.arguments import add_arg
import datetime

# SETUP
DEFAULT_GENERATORS_FILE = "mock_generators/generators.json"
filename = DEFAULT_GENERATORS_FILE

# UI
st.title("Mock Graph Data Generators")
st.write("This is a collection of mock data generators for generating mock graph data in a mockgraphdata app")

tab1, tab2, tab3 = st.tabs(["Config", "Generators", "Create"])
with tab1: 
    st.write("Configuration Options")
    filename = st.text_input("Generators filepath", filename)
    try:
        with open(filename) as input:
            generators_file = input.read()
            generators_json = load_json(filename)
            generators = generators_from_json(generators_json)
    except FileNotFoundError:
        st.error('File not found.')
    with st.expander("Generators JSON"):
        st.text(generators_file)

with tab2:
    st.write("List of available mock data generators")
    # logging.info(f"Generators: {generators}")
    for key in generators:
        generator = generators[key]
        # logging.info(f"Generator: {generator}")
        with st.expander(generator.name):
            st.write(f"Description:\n {generator.description}")
            st.write(f'Generator Code:\n')

            # Display generator code
            code_filepath = generator.code_url
            code_file = load_string(code_filepath)
            st.text(code_file)
            args = generator.args
            arg_inputs = []
            for arg in args:
                if arg.type == GeneratorType.STRING:
                    arg_inputs.append(st.text_input(
                        label=arg.label, 
                        value = arg.default,
                        key = f'{generator.id}_{arg.label}'
                        ))
                if arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                    arg_inputs.append(st.number_input(
                        label= arg.label,
                        value= arg.default,
                        key = f'{generator.id}_{arg.label}'
                        ))
                if arg.type == GeneratorType.BOOL:
                    arg_inputs.append(st.radio(
                        label=arg.label,
                        index=arg.default,
                        key = f'{generator.id}_{arg.label}'
                    ))
                if arg.type == GeneratorType.DATETIME:
                    arg_inputs.append(st.date_input(
                        label=arg.label,
                        value=datetime.datetime.fromisoformat(arg.default),
                        key = f'{generator.id}_{arg.label}'
                    ))
                # TODO: Datetime
            if st.button("GenerateExample Output", key=f"run_{generator.id}"):
                module = __import__(generator.import_url(), fromlist=['generate'])
                # logging.info(f'arg_inputs: {arg_inputs}')
                result = module.generate(arg_inputs)
                st.write(f'Output: {result}')

with tab3:
    st.write("Create a new mock data generator")
    # Make radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    type = st.radio("Generator Type", ["String", "Bool", "Int", "Float","Datetime"])
    name = st.text_input("Generator Name")
    description = st.text_input("Generator Description")
    code_template = generic_template()
    code = st.text_area("Generator Code", placeholder = code_template, height = 200, value = code_template)
    if type == "String":
        logging.info('String')
    if type == "Bool":
        logging.info('Bool')

    # Arguments
    num_cols = st.number_input("Number of Arguments", 0)
    args = []
    def arg_callback(arg_dict):
        if arg_dict:
            args.append(arg_dict)

    if num_cols > 0:
        cols = st.columns(num_cols)
        for i in range(num_cols):
            st.markdown("""---""")
            add_arg(i, arg_callback)

    if st.button("Create Generator"):
        st.write("Creating generator...")
        success = createGenerator(
            existing=generators, 
            type=type, 
            name=name, 
            description=description, 
            code=code,
            args=args)
        if success:
            st.success("Generator created successfully")
        else:
            st.error("Could not create generator")
        
