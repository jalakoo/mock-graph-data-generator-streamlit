import streamlit as st
from constants import *
import logging
from models.generator import Generator, GeneratorType, recommended_generator_from
from models.property_mapping import PropertyMapping
import datetime
from widgets.default_state import load_state
import sys

load_state()

def generators_filtered(
    generators: list[Generator],
    byTypes: list[GeneratorType]
    ) -> list[Generator]:

    # generators = st.session_state[GENERATORS]
    result =  [generator for _, generator in generators.items() if generator.type in byTypes]
    def sort_by_name(generator: Generator):
        return generator.name
    result.sort(key=sort_by_name)
    return result

def property_row(
    type: str,
    id: str,
    index: int, 
    properties: list,
    generators: list[Generator]) -> PropertyMapping:

    # gens = st.session_state[GENERATORS]
    # if gens is None:
    #     load_state()
    # # Check again
    # if st.session_state[GENERATORS] is None:
    #     st.error("Could not load generators. Check generator file paths.")
    #     return PropertyMapping.empty()

    # gen_values = gens.values()
    # Properties is a list of dictionaries 

    # Create a new propertyMapping for storing user selections
    pc1, pc2, pc3, pc4, pc5, pc6 = st.columns(6)
    
    # Property name
    with pc1:
        existing_name = ""
        recommended_generator = None
        if index < len(properties):
            # Get key of uploaded property
            existing_name = properties[index][0]
            recommended_generator = recommended_generator_from(existing_name, generators.values())
            # logging.info(f'recommended generator for property name: {existing_name}: {recommended_generator}')
        name = st.text_input("Property Name",value=existing_name, key=f"{type}_{id}_property_{index}_name")
        if name != "" and name[0] == "_":
            st.error("Property names cannot start with an underscore")
            name = None

    # Property type
    with pc2:
        type_selections = ["String", "Bool", "Integer", "Float", "Datetime"]
        recommended_type_index = 0
        if recommended_generator != None:
            recommended_type_index = type_selections.index(recommended_generator.type.to_string())
        generator_type_string = st.selectbox("Type", type_selections, index=recommended_type_index, key=f"{type}_{id}_property_{index}_type")
        generator_type = GeneratorType.type_from_string(generator_type_string)

    # Generator to create property data with
    with pc3:
        recommended_generator_index = 0
        possible_generators = generators_filtered(generators,[generator_type])
        possible_generator_names = [generator.name for generator in possible_generators]

        if recommended_generator is not None:
            try:
                recommended_generator_index = possible_generator_names.index(recommended_generator.name)
            except ValueError:
                # This shouldn't happen since we chose the type above
                logging.error(f'Generator {recommended_generator.name} type did not match selected generator type: {generator_type}')
            except:
                logging.error(f'Unexpected error while trying to find recommended generator: {recommended_generator.name}: {sys.exc_info()[0]}')
        selected_generator_name = st.selectbox("Generator", possible_generator_names, index=recommended_generator_index, key=f"{type}_{id}_property_{index}_generator", help="See the Generators Tab for more details on a given generator.")

        selected_generators = [generator for generator in possible_generators if generator.name == selected_generator_name]
        if len(selected_generators) == 0:
            st.error(f'No generator found for {selected_generator_name}')
            selected_generator = None
        else:
            selected_generator = selected_generators[0]


    # Optional Property Generator arguments, if any
    with pc4:
        args = []
        if selected_generator is not None:
            for p_index, arg in enumerate(selected_generator.args):
                if arg.type == GeneratorType.STRING:
                    arg_input = st.text_input(
                        label=arg.label, 
                        value = arg.default,
                        key = f'{type}_{id}_property_{name}_generator_{selected_generator.id}_{arg.label}'
                        )
                elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                    arg_input = st.number_input(
                        label= arg.label,
                        value= arg.default,
                        key = f'{type}_{id}_property_{name}_generator_{selected_generator.id}_{arg.label}'
                        )
                elif arg.type == GeneratorType.BOOL:
                    arg_input = st.radio(
                        label=arg.label,
                        index=arg.default,
                        key = f'{type}_{id}_property_{name}_generator_{selected_generator.id}_{arg.label}'
                    )
                    # arg_inputs.append()
                elif arg.type == GeneratorType.DATETIME:
                    arg_input = st.date_input(
                        label=arg.label,
                        value=datetime.datetime.fromisoformat(arg.default),
                        key = f'{type}_{id}_property_{name}_generator_{selected_generator.id}_{arg.label}')
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
        if selected_generator is not None:
            result = selected_generator.generate(property_map.args)
            st.write(f'Sample')
            st.text(f'{result}')
    
    with pc6:
        st.write("Options")
        should_ignore = st.checkbox("Exclude/ignore", value=False,  key=f"{type}_{id}_property_{index}__ignore")

    if should_ignore == True:
        return PropertyMapping.empty()
        
    return property_map