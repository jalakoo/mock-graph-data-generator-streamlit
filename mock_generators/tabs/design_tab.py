import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from constants import *
from file_utils import load_string
import sys
import logging
import datetime
from models.generator import GeneratorType
import pyperclip
import json

def design_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/abstract.gif")
    with col2:
        st.write(f"Design Data Model.\n\nUse the [arrows.app](https://arrows.app) then download the .json file to the Import tab.")
    st.markdown("--------")

    c1, c2 = st.columns([8,2])
    with c1:
        components.iframe("https://arrows.app", height=1000, scrolling=False)
    with c2:
        st.write("Generators")
        st.markdown("--------")
        # TODO: Put generators search feature here
        # TODO: Add copy and paste button to produce specially formatted string values to use in the arrows property app

        generators = st.session_state[GENERATORS]
        if generators is None:
            st.write("No generators loaded")
            st.stop()

        # Search by name or description
        search_term = st.text_input("Search by keyword", "")

        # Filter by type
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        type_filter = st.radio("Filter by type", ["All", "String", "Bool", "Integer", "Float","Datetime", "Assignment"])
        # logging.info(f"Generators: {generators}")
        for _, generator in sorted(generators.items(), key=lambda gen:(gen[1].name)):
            # generator = generators[key]
            # Filtering
            if type_filter != "All" and type_filter != generator.type.to_string():
                continue

            if search_term != "" and search_term.lower() not in generator.name.lower() and search_term.lower() not in generator.description.lower():
                continue
            
            try:
                # Check that we can load code first
                code_filepath = generator.code_url
                code_file = load_string(code_filepath)
            except:
                logging.error(f"Could not load generator code from {code_filepath}: {sys.exc_info()[0]}") 
                continue

            with st.expander(generator.name):
                st.write(f"\n {generator.description}")
                # st.write(f'Generator Code:\n')
                # st.markdown(f'```python\n{code_file}\n```')
                args = generator.args
                arg_inputs = []
                for arg in args:
                    if arg.type == GeneratorType.STRING:
                        arg_inputs.append(st.text_input(
                            label=arg.label, 
                            value = arg.default,
                            key = f'{generator.id}_{arg.label}',
                            placeholder = f'{arg.hint}',
                            help = f'{arg.description}'
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
                if st.button("Generate Example Output", key=f"run_{generator.id}"):
                    try:
                        module = __import__(generator.import_url(), fromlist=['generate'])
                        # logging.info(f'arg_inputs: {arg_inputs}')

                        # TODO: Need a fake list of Node Mappings to test out assignment generators
                        result = module.generate(arg_inputs)
                        st.write(f'Output: {result}')
                    except:
                        st.error(f"Problem running generator {generator.name}: {sys.exc_info()[0]}")
                if st.button("Copy for Arrows", key=f"copy_{generator.id}"):
                    name = generator.name
                    args = arg_inputs
                    obj = {
                        generator.id: args
                    }
                    json_string = json.dumps(obj)
                    pyperclip.copy(json_string)
                    st.success(f'Copied to clipboard: {json_string}. Paste into Arrows.app to use.')