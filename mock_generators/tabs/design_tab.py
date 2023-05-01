import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.colored_header import colored_header
from constants import *
from file_utils import load_string
import sys
import logging
import datetime
from models.generator import GeneratorType
# import pyperclip
import json

def design_tab():

    # col1, col2 = st.columns([1,11])
    # with col1:
    #     st.image("mock_generators/media/abstract.gif")
    # with col2:
    #     st.write(f"Design Data Model.\n\nUse the [arrows.app](https://arrows.app) then download the .json file to the Import tab.")
    # st.markdown("--------")
    with st.expander("Instructions"):
        st.write("""
        1. Connect to arrows.app. Optionally login via Google to save your model designs
        2. Select a Node or Relationship to display a properties inspector on the right
        3. Configure the mock graph generator by adding properties with specially formatted keys and value strings. See additional details on how to do this in the dropdowns below
        4. Once completed, click on the 'Download/Export' button in the arrows.app. Make sure to use the 'JSON' export option
        5. Proceed to the '② Generate' tab
        """)
    d1, d2, d3 = st.columns(3)
    with d1:
        with st.expander("NODE requirements"):
            st.write("Nodes require 2 keys to have mock data generated for it:  {count} and {key}. The {count} key identifies which data generator (and args) to use for creating the number of nodes.\n\nExample of node properties that would create mock data:")
            st.image("mock_generators/media/sample_node_properties.png")
    with d2:
        with st.expander("RELATIONSHIP requirements"):
            st.write("Relationships require 1 key: {count} and can take 2 optional keys: {assignment} and {filter}. The {count} key identifies which data generator (and args) to use for creating the number of relationships between a source node and a target node. EXAMPLE: If every source node should connect to exactly one target node, then the target generator value should be 1.\n\nThe {assignement} key identifies which data generator (and args) to use when deciding which target nodes this relationship should connect with.\n\nThe {filter} key identifies a data generator (and args) to use for deciding what, if any, target nodes to ignore.\n\nExample of node properties that would create mock data:")
            st.image("mock_generators/media/sample_relationship_properties.png")
    with d3:
        with st.expander("PROPERTY requirements"):
            st.write("Properties needing mock generated data should be a stringified JSON object. The unique generator name should be used as a key, followed by a list/array or argument values.\n\nSee the NODE and RELATIONSHIP properties dropdown for examples.\n\nThe right hand Generators preview lists all the available mock data generators. Arguments can be set and example output data can be previewed by clicking on the 'Generate Example Output' button. Use the 'Copy for Arrows' button to copy the required formatted JSON string to your clipboard, to paste into the arrows.app")
            st.image("mock_generators/media/sample_generator.png")

    c1, c2 = st.columns([8,2])
    with c1:
        components.iframe("https://arrows.app", height=1000, scrolling=False)
    with c2:
        # st.write("Generators")
        # st.markdown("--------")

        generators = st.session_state[GENERATORS]
        if generators is None:
            st.write("No generators loaded")
            st.stop()

        # Search by name or description
        search_term = st.text_input("Search Generators by keyword", "", help="Generators are functions for creating mock data.")

        # Filter by type
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        type_filter = st.radio("Filter Generator outputs by type", ["All", "String", "Bool", "Integer", "Float","Datetime", "Assignment"])
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

                # Property Code
                # name = generator.name
                args = arg_inputs
                obj = {
                    generator.id: args
                }

                json_string = json.dumps(obj, default=str)


                st.write('Copy & paste below as a node/relationship property value in arrows.app')
                # copy1, copy2 = st.columns(2)
                # with copy1:
                st.code(f'{json_string}')

                # Paperclip / copy in general known to not work in streamlit cloud
                # with copy2:
                #     if st.button("Copy for Arrows", key=f"copy_{generator.id}"):
                #         pyperclip.copy(json_string)
                #         st.success(f'Copied to clipboard: {json_string}. Paste as a property value in Arrows.app')
