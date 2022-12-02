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
    # property_map = PropertyMapping(id=f'{type}_{id}_property_{index}')
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
        # if name in [property_map.name for property_map in property_maps]:
        #     st.error("Property names must be unique")
        #     property_map.name = None
        # else:
        #     name = name

    # Property type
    with pc2:
        type_string = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"{type}_{id}_property_{index}_type")
        type = GeneratorType.type_from_string(type_string)
        # type = type

    # Generator to create property data with
    with pc3:
        possible_generators = generators_filtered([type])
        possible_generator_names = [generator.name for generator in possible_generators]
        selected_generator_name = st.selectbox("Generator", possible_generator_names, key=f"{type}_{id}_property_{index}_generator")

        selected_generator = [generator for generator in possible_generators if generator.name == selected_generator_name][0]

        # property_map.generator = selected_generator

    # Optional Property Generator arguments, if any
    with pc4:
        args = []
        if selected_generator is not None:
            # if selected_generator.args == []:
            #     property_map.args.clear()
            # else:
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

                # logging.info(f'arg_input: {arg_input}')
                args.append(arg_input)

        property_map = PropertyMapping(
            id=f'{type}_{id}_property_{index}',
            name=name,
            type=type,
            generator=selected_generator,
            args=args
        )


    # Display sample data
    with pc5:
        result = selected_generator.generate(property_map.args)
        st.write(f'Sample')
        st.text(f'{result}')

    return property_map