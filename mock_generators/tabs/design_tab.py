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

    with st.expander("Instructions"):
        st.write("""
        1. Connect to arrows.app. Optionally login via Google to save your model designs
        2. Select a Node or Relationship to display a properties inspector on the right
        3. Configure the mock graph generator by adding properties with specially formatted keys and value strings. See additional details on how to do this in the dropdowns below
        4. Once completed, click on the 'Download/Export' button in the arrows.app. Make sure to use the 'JSON' export option
        5. Proceed to the '③ Generate' tab
        """)
    d1, d2, d3 = st.columns(3)
    with d1:
        with st.expander("NODE Options"):
            st.write("Add a COUNT key to identify how many of a given node you'd like created. Use a KEY key to notate which other property field you'd like use a unique identifier for a node type.\n\nExample of node properties for specifying specific number of nodes with particular properties:")
            st.image("mock_generators/media/sample_node_0-5-0.png")
    with d2:
        with st.expander("RELATIONSHIP Options"):
            st.write("Relationships can take 2 optional keys: COUNT and ASSIGNMENT to specify how many of a given relationship should be created and what assignment generator should be used")
            st.image("mock_generators/media/sample_relationship_0-5-0.png")
    with d3:
        with st.expander("PROPERTY Options"):
            st.write("Properties needing mock generated data can be a stringified JSON object representing a generator specification. Literals such as numbers, number ranges, and list of options can also be used. For example: 1, 1.0, 1-10, 3.3-4.5, [1,2,3], [1.0, 2.2, 3.3], a_word, [word1, word2, word3] are valid values. General types can also be used, such as string, integer, float, boolean, and datetime.")
            st.image("mock_generators/media/sample_properties_0-5-0.png")

    
    c1, c2 = st.columns([8,2])
    with c1:
        # Arrows interface
        components.iframe("https://arrows.app", height=1000, scrolling=False)
    with c2:
        # Generators List
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
