import streamlit as st
from models.generator import Generator, GeneratorType
import logging

def generator_selector(
    label: str,
    generators: list[Generator],
    key: str,
    types: list[GeneratorType] = []
    ) -> Generator:
    """
    Returns a generator selected from a dropdown list of generators.
    """

    # List comprehension not working on hot reloads

    possible_generators = [generator for _, generator in generators.items() if generator.type in types]
    if possible_generators is None:
        st.error("No possible generators found for type INT.")
        logging.error(f'generator_selector.py: No possible generators found for types {types}. Received generators: {generators}')
        st.stop()

    possible_generator_names = [generator.name for generator in possible_generators]
    possible_generator_names.sort(reverse=False)

    selected_generator_name = st.selectbox(
        label=label, 
        options=possible_generator_names, 
        key=key)

    possible_selected_generators =[generator for generator in possible_generators if generator.name == selected_generator_name]
    if len(possible_selected_generators) == 0:
        st.error(f'Generator "{selected_generator_name}" not found.')
        st.stop()
    
    selected_generator = possible_selected_generators[0]
    return selected_generator