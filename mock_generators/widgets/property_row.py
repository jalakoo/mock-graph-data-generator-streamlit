import streamlit as st
from constants import *
import logging
from models.generator import Generator, GeneratorType
from models.property_mapping import PropertyMapping
import datetime

def generators_filtered(byTypes: list[GeneratorType]) -> list[Generator]:
    generators = st.session_state[GENERATORS]
    return [generator for _, generator in generators.items() if generator.type in byTypes]

def property_row(
    type: str,
    id: str,
    index: int, 
    properties: dict) -> PropertyMapping:

    # Create a new propertyMapping for storing user selections
    pc1, pc2, pc3, pc4, pc5 = st.columns(5)

    # Property name
    with pc1:
        existing_name = ""
        if index < len(properties):
            # Get key of property
            existing_name = properties[index][0] 
        name = st.text_input("Property Name",value=existing_name, key=f"{type}_{id}_property_{index}_name")
        if name != "" and name[0] == "_":
            st.error("Property names cannot start with an underscore")
            name = None

    # Property type
    with pc2:
        generator_type_string = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"{type}_{id}_property_{index}_type")
        generator_type = GeneratorType.type_from_string(generator_type_string)

    # Generator to create property data with
    with pc3:
        possible_generators = generators_filtered([generator_type])
        possible_generator_names = [generator.name for generator in possible_generators]
        selected_generator_name = st.selectbox("Generator", possible_generator_names, key=f"{type}_{id}_property_{index}_generator")

        selected_generator = [generator for generator in possible_generators if generator.name == selected_generator_name][0]


    # Optional Property Generator arguments, if any
    with pc4:
        args = []
        if selected_generator is not None:
            for p_index, arg in enumerate(selected_generator.args):
                if arg.type == GeneratorType.STRING:
                    arg_input = st.text_input(
                        label=arg.label, 
                        value = arg.default,
                        key = f'{type}_{id}_property_{p_index}_generator_{selected_generator.id}_{arg.label}'
                        )
                elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                    arg_input = st.number_input(
                        label= arg.label,
                        value= arg.default,
                        key = f'{type}_{id}_property_{p_index}_generator_{selected_generator.id}_{arg.label}'
                        )
                elif arg.type == GeneratorType.BOOL:
                    arg_input = st.radio(
                        label=arg.label,
                        index=arg.default,
                        key = f'{type}_{id}_property_{p_index}_generator_{selected_generator.id}_{arg.label}'
                    )
                    # arg_inputs.append()
                elif arg.type == GeneratorType.DATETIME:
                    arg_input = st.date_input(
                        label=arg.label,
                        value=datetime.datetime.fromisoformat(arg.default),
                        key = f'{type}_{id}_property_{p_index}_generator_{selected_generator.id}_{arg.label}')
                else:
                    logging.error(f'Unknown argument type {arg.type}')
                    arg_input = None

                args.append(arg_input)

        property_map = PropertyMapping(
            id=f'{type}_{id}_property_{index}',
            name=name,
            type=generator_type,
            generator=selected_generator,
            args=args
        )


    # Display sample data
    with pc5:
        result = selected_generator.generate(property_map.args)
        st.write(f'Sample')
        st.text(f'{result}')

    return property_map