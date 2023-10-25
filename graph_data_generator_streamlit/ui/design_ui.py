import streamlit as st
import streamlit.components.v1 as components
from graph_data_generator import generators, GeneratorType, Generator

import os
import logging
import datetime
import json
import sys
import io

def load_string(filepath: str, default=None):
    if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
         with io.open(os.path.join(filepath), 'r') as _:
            logging.info(f"file_utils.py: No file at {filepath}")
            return default
    with open(filepath, 'r') as f:
        return f.read()

def filtered_generators(
        search_term: str, 
        type_filter: str,
        generators: dict[str, Generator]):
    
    def passes_search(search_term: str, 
                      generator: Generator):
        if search_term is None:
            return True
        if search_term != "" and search_term.lower() not in generator.name.lower() and search_term.lower() not in generator.description.lower():
            return False
        return True
    
    def passes_type_filter(type_filter: str,
                           generator: Generator):
        if type_filter != "All" and type_filter != generator.type.to_string():
            return False
        return True
    
    return [generator for key, generator in sorted(generators.items(), key=lambda gen:(gen[1].name)) if passes_search(search_term, generator) and passes_type_filter(type_filter, generator)]

# Why isn't this working outside of this class files?
def generators_ui():
    search_term = st.text_input("Search Generators by keyword", "", help="Generators are functions for creating mock data.")
    # st.write(generators)
    type_filter = st.radio("Filter Generator outputs by type", ["All", "String", "Bool", "Integer", "Float", "Function", "Datetime", "Assignment"], index=0)
    
    total_count = len(generators)
    display_generators = filtered_generators(search_term, type_filter, generators)
    count = len(display_generators)
    st.write(f"Displaying {count} of {total_count} generators:")
    for generator in display_generators:

        with st.expander(generator.name):
        # st.markdown("------------------")
            st.write(generator.name)
            st.write(f"\n {generator.description}")
            args = generator.args
            arg_inputs = []
            for arg in args:
                if arg.type == GeneratorType.STRING:
                    arg_inputs.append(st.text_input(
                        label=arg.label, 
                        value = arg.default,
                        key = f'{generator.name}_{arg.label}',
                        placeholder = f'{arg.hint}',
                        help = f'{arg.description}'
                        ))
                if arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                    arg_inputs.append(st.number_input(
                        label= arg.label,
                        value= arg.default,
                        key = f'{generator.name}_{arg.label}'
                        ))
                if arg.type == GeneratorType.BOOL:
                    arg_inputs.append(st.radio(
                        label=arg.label,
                        index=arg.default,
                        key = f'{generator.name}_{arg.label}'
                    ))
                if arg.type == GeneratorType.DATETIME:
                    arg_inputs.append(st.date_input(
                        label=arg.label,
                        value=datetime.datetime.fromisoformat(arg.default),
                        key = f'{generator.name}_{arg.label}'
                    ))
            # if c.button("Generate Example Output", key=f"run_{generator.name}"):
            #     try:
            #         module = __import__(generator.import_url(), fromlist=['generate'])
            #         # logging.info(f'arg_inputs: {arg_inputs}')

            #         # TODO: Need a fake list of Node Mappings to test out assignment generators
            #         result = module.generate(arg_inputs)
            #         c.write(f'Output: {result}')
            #     except:
            #         c.error(f"Problem running generator {generator.name}: {sys.exc_info()[0]}")

            # Property Code
            # name = generator.name
            args = arg_inputs
            obj = {
                generator.gid: args
            }

            json_string = json.dumps(obj, default=str)

            st.write('Copy & paste below as a node/relationship property value in arrows.app')

            # st.code widgets automatically include a copy and paste button
            st.code(f'{json_string}')
            
def arrows_ui():
    st.markdown(
        """
        Use the arrows app to quickly design your mock data. When ready, click on the `Download/Export` button, select the `JSON` tab, then copy the .JSON data to the **② Generate** section
        """
    )
    # TODO: Read from state if a graphGPT model has been created and load that

    uri = "https://arrows.app"
    if "ARROWS_URI" in st.session_state:
        prior_uri = st.session_state["ARROWS_URI"]
        if prior_uri is not None:
            uri = prior_uri

    components.iframe(uri, height=1000, scrolling=False)

    st.session_state["ARROWS_URI"] = None