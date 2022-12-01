import streamlit as st
from constants import *
import uuid
from models.property_mapping import PropertyMapping
from models.generator import Generator, GeneratorType
from models.relationship_mapping import RelationshipMapping
import datetime

def generators_filtered(byTypes: list[GeneratorType]) -> list[Generator]:
    generators: list[Generator] = st.session_state[GENERATORS]
    return [generator for _, generator in generators.items() if generator.type in byTypes]

def relationship_row(relationship: dict):

    # Sample relationship dict from arrows.app
    # {
    #   "id": "n0",
    #   "type": "WORKS_AT",
    #   "style": {},
    #   "properties": {
    #     "created_at": "datetime"
    #   },
    #   "fromId": "n0",
    #   "toId": "n1"
    # }

    if relationship is None:
        id = str(uuid.uuid4())[:8]
        type = ""
        properties = []
        fromId = ""
        toId = ""
    else:
        id = relationship.get("id", str(uuid.uuid4())[:8])
        type = relationship.get("type","")
        fromId = relationship.get("fromId")
        toId = relationship.get("toId")
        if 'properties' in relationship:
            properties = [(k,v) for k,v in relationship.get("properties").items()]
        else:
            properties = []

    with st.expander(f"relationship id: {id}, type: {type}, from: {fromId}, to: {toId}"):

        # Relationship type
        st.markdown('---')
        new_type = st.text_input("Type", value=type, key=f"relationship_{id}_type")

        if new_type != type:
            type = new_type

        # Relationship nodes
        st.markdown('---')
        r1, r2 = st.columns(2)

        # TODO: Update to use selectbox instead.
        with r1:
            # Relationship from
            new_fromId = st.text_input("From Node", value=fromId, key=f"relationship_{id}_fromId")
            if new_fromId != fromId:
                fromId = new_fromId
        with r2:
            # Relationship to
            new_toId = st.text_input("To Node", value=toId, key=f"relationship_{id}_toId")
            if new_toId != toId:
                toId = new_toId

        # Relationship properties
        st.markdown('---')
        num_properties = st.number_input("Number of properties", min_value=0, value=len(properties), key=f"relationship_{id}_number_of_properties")

        property_maps = []
        for i in range(num_properties):
            # Create a new propertyMapping for storing user selections
            property_map = PropertyMapping(id=f'relationship_{id}_property_{i}')
            pc1, pc2, pc3, pc4, pc5 = st.columns(5)

            # Property name
            with pc1:
                existing_name = ""
                if i < len(properties):
                    # Get key of property
                    existing_name = properties[i][0] 
                name = st.text_input("Property Name",value=existing_name, key=f"relationship_{id}_property_{i}_name")
                property_map.name = name

            # Property type
            with pc2:
                property_type_string = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"relationship_{id}_property_{i}_type")
                property_type = GeneratorType.type_from_string(property_type_string)
                property_map.type = property_type

            # Generator to create property data with
            with pc3:
                possible_generators = generators_filtered([property_type])
                possible_generator_names = [generator.name for generator in possible_generators]

                selected_generator_name = st.selectbox("Generator", possible_generator_names, key=f"relationship_{id}_property_{i}_generator")

                selected_generator = None
                if selected_generator_name != "" and selected_generator_name is not None:
                    selected_generator = next(generator for generator in possible_generators if generator.name == selected_generator_name)
                    property_map.generator = selected_generator

            # Optional Generator arguments, if any
            with pc4:
                if selected_generator is not None:
                    if selected_generator.args == []:
                        property_map.args.clear()
                    else:
                        for p_index, arg in enumerate(selected_generator.args):
                            if arg.type == GeneratorType.STRING:
                                arg_input = st.text_input(
                                    label=arg.label, 
                                    value = arg.default,
                                    key = f'relationship_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                    )
                            elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                                arg_input = st.number_input(
                                    label= arg.label,
                                    value= arg.default,
                                    key = f'relationship_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                    )
                            elif arg.type == GeneratorType.BOOL:
                                arg_input = st.radio(
                                    label=arg.label,
                                    index=arg.default,
                                    key = f'relationship_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                )
                                # arg_inputs.append()
                            elif arg.type == GeneratorType.DATETIME:
                                arg_input = st.date_input(
                                    label=arg.label,
                                    value=datetime.datetime.fromisoformat(arg.default),
                                    key = f'relationship_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}')
                            else:
                                arg_input = None

                            # Save argument values
                            if p_index < len(property_map.args):
                                property_map.args[p_index] = arg_input
                            else:
                                property_map.args.append(arg_input)


                # Save options for generating mock property data later
                property_maps.append(property_map)
                        
            with pc5:
                # Display sample data
                if selected_generator is not None:
                    st.write(f'Sample')
                    st.text(f'{selected_generator.generate(property_map.args)}')
        

        # Relationships to generate
        st.markdown('---')
        st.write('Number of these relationships to generate')
        possible_count_generators = generators_filtered([GeneratorType.INT])
        possible_count_generator_names = [generator.name for generator in possible_count_generators]

        ncc1, ncc2, ncc3 = st.columns(3)

        with ncc1:
            selected_count_generator_name = st.selectbox("Int Generator to use", possible_count_generator_names, key=f"relationship_{id}_count_generator")
            selected_count_generator = next(generator for generator in possible_count_generators if generator.name == selected_count_generator_name)
        with ncc2:
            count_arg_inputs = []
            if selected_count_generator is not None:
                for count_index, arg in enumerate(selected_count_generator.args):
                    if arg.type == GeneratorType.STRING:
                        count_arg = st.text_input(
                            label=arg.label, 
                            value = arg.default,
                            key = f'relationship_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            )
                    elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                        count_arg = st.number_input(
                            label= arg.label,
                            value= arg.default,
                            key = f'relationship_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            )
                    elif arg.type == GeneratorType.BOOL:
                        count_arg = st.radio(
                            label=arg.label,
                            index=arg.default,
                            key = f'relationship_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                        )
                    elif arg.type == GeneratorType.DATETIME:
                        count_arg = st.date_input(
                            label=arg.label,
                            value=datetime.datetime.fromisoformat(arg.default),
                            key = f'relationship_{id}_count_generator_{selected_count_generator.id}_{arg.label}')
                    else:
                        count_arg = None
                    if count_arg is not None:
                        if count_index >= len(count_arg_inputs):
                            count_arg_inputs.append(count_arg)
                        else:
                            count_arg_inputs[count_index] = count_arg
        with ncc3:
            disabled = st.checkbox("Exclude/ignore relationship", value=False, key=f"relationship_{id}_enabled")
            if disabled:
                # Remove from mapping
                mapping = st.session_state[MAPPINGS]
                mapping_relationships = mapping.relationships
                if id in mapping_relationships:
                    del mapping_relationships[id]
                    mapping.relationships = mapping_relationships
                    st.session_state[MAPPINGS] = mapping
                st.warning(f'Relationship EXCLUDED from mapping')
            else:
                mapping = st.session_state[MAPPINGS]
                relationships = mapping.relationships
                relationship_mapping = RelationshipMapping(
                    id=id,
                    type=type,
                    start_node_id=fromId,
                    end_node_id=toId,
                    count_generator=selected_count_generator,
                    count_args=count_arg_inputs,
                    properties=property_maps
                )
                relationships[id] = relationship_mapping
                mapping.relationships = relationships
                st.session_state[MAPPINGS] = mapping
                st.info(f'Relationship added to mapping')
          