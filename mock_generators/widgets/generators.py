import streamlit as st
from models.generator import Generator, GeneratorType
from file_utils import load_string
import datetime
import logging
import sys

def generators_tab(
    generators: list[Generator], 
    code_filepath: str):
    if generators is None:
        st.write("No generators loaded")
        return

    st.write("List of available mock data generators")

    # Search by name or description
    search_term = st.text_input("Search by keyword", "")

    # Filter by type
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    type_filter = st.radio("Filter by type", ["All", "String", "Bool", "Int", "Float","Datetime"])
    # logging.info(f"Generators: {generators}")
    for key in generators:
        generator = generators[key]
        # Filtering
        if type_filter != "All" and type_filter != generator.type.to_string():
            continue

        if search_term != "" and search_term.lower() not in generator.name.lower() and search_term.lower() not in generator.description.lower():
            continue
        
        # logging.info(f"Generator: {generator}")
        try:
            # Check that we can load code first
            code_filepath = generator.code_url
            code_file = load_string(code_filepath)

            with st.expander(generator.name):
                st.write(f"Description:\n {generator.description}")
                st.write(f'Generator Code:\n')

                # Display generator code
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
                if st.button("GenerateExample Output", key=f"run_{generator.id}"):
                    module = __import__(generator.import_url(), fromlist=['generate'])
                    # logging.info(f'arg_inputs: {arg_inputs}')
                    result = module.generate(arg_inputs)
                    st.write(f'Output: {result}')
        except:
            continue
            logging.error(f"Could not load generator code from {code_filepath}: {sys.exc_info()[0]}")