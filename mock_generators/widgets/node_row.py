import streamlit as st
from constants import *
from widgets.property_row import property_row
from models.generator import Generator, GeneratorType
from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
import uuid
import datetime
import logging

def generators_filtered(byTypes: list[GeneratorType]) -> list[Generator]:
    generators = st.session_state[GENERATORS]
    return [generator for _, generator in generators.items() if generator.type in byTypes]

def nodes_row(
    node: dict,
    should_start_expanded: bool = False,
    additional_properties: list[PropertyMapping] = []
    ):

    #  Sample node dict from arrows.app
    # {
    # "id": "n0",
    # "position": {
    #     "x": -306.93969052033395,
    #     "y": 271.3634778613202
    # },
    # "caption": "Person",
    # "labels": [],
    # "properties": {
    #     "email": "string",
    #     "salary_usd": "int",
    #     "first_name": "string",
    #     "last_name": "string"
    # },
    # "style": {}
    # }

    if node is not None:
        # Load node data from an imported dict
        id = node.get("id")
        labels = node.get("labels", [])
        position = {
            "x": node.get("position", {}).get("x", 0),
            "y": node.get("position", {}).get("y", 0)
        }
        caption = node.get("caption", "")
        properties = [(k,v) for k,v in node.get("properties").items()]
        selected_labels = labels
    else:
        # Use a default empty node
        id = str(uuid.uuid4())[:8]
        labels = ["<add_label>"]
        position = {
            "x": 0,
            "y": 0
        }
        caption = ""
        properties = []
        selected_labels = []

    # Create an expandable list item for each node
    with st.expander(f"NODE {id} - {caption}", expanded=should_start_expanded):
        st.markdown('---')

        nc1, nc2, nc3, nc4 = st.columns(4)

        # Display/edit Caption
        with nc1:
            new_caption = st.text_input(
            f"Primary Label", 
            value = caption,
            key=f"node_{id}_primary_label")
            if new_caption != caption:
                caption = new_caption

        # Adjust number of labels
        with nc2:
            num_labels = st.number_input("Number of Additional labels", min_value=0, value=len(labels), key=f"node_{id}_num_labels", help="Nodes may have more than one label. Select the number of additional labels to add.")
        if num_labels > 0:
            label_columns = st.columns(num_labels)
            for li, x in enumerate(label_columns):
                loaded_label = ""
                if li < len(labels):
                    loaded_label = labels[li]
                new_label = x.text_input(
                    f"Label {li + 1}", 
                    value = loaded_label,
                    key=f"node_{id}_label_{li}")
                if new_label != "" and new_label not in labels and new_label is not None:
                    if li < len(labels):
                        selected_labels[li] = new_label
                    else:
                        selected_labels.append(new_label)

        with nc3:
            initial_num_properties = len(properties)
            # All nodes should have at least one property
            # Otherwise we're just generating a bunch of empty nodes
            # which doesn't require a mock data generator to do. But
            # whatever, maybe someone needs a few label only nodes
            num_properties = st.number_input("Number of properties", value = initial_num_properties, min_value=0, key= f'node_{id}_num_properties', help="Nodes typically have one or more properties. Select the number of properties for this node.")

        with nc4:
            st.write('Options')
            disabled = st.checkbox("Exclude/ignore node", value=False, key=f"node_{id}_disabled")

        # Adjust number of properties 
        st.markdown('---')
        initial_num_properties = len(properties)

        # Generate input fields for user to adjust property names, types, and generator to create mock data with

        property_maps = {}

        for i in range(num_properties):

            new_property_map = property_row(
                type="node", 
                id=id, 
                index=i, 
                properties= properties)

            if new_property_map.id == None:
                # Equal to an empty PropertyMapping - likely been explicitly excluded by user
                continue

            if new_property_map.name in property_maps:
                st.error(f'Property "{new_property_map.name}" already exists')
            else:
                property_maps[new_property_map.name] = new_property_map

        # TODO: Investigate. If the below block is moved above the range block above, then the relationship.csv generated will use the first of the global properties as a key instead of the node's proper key property.

        # Load any additional properties that were passed in
        if additional_properties != None and len(additional_properties) > 0:
            for additional_property in additional_properties:
                property_maps[additional_property.name] = additional_property

        st.markdown('---')
        key_property_name = st.selectbox("Key Property", property_maps.keys(), key=f'node_{id}_key_property', help="Property value that uniquely identifies these nodes from other nodes")
        if key_property_name not in property_maps:
            st.error(f'Property "{key_property_name}" does not exist in properties for node {caption}')
            selected_key_property = None
        else:
            selected_key_property = property_maps[key_property_name]

        # property_maps.append(new_property_map)


        st.markdown('---')
        st.write(f'Number of {caption} records to generate')
        possible_count_generators = generators_filtered([GeneratorType.INT])
        possible_count_generator_names = [generator.name for generator in possible_count_generators]

        ncc1, ncc2 = st.columns(2)

        with ncc1:
            selected_count_generator_name = st.selectbox("Int Generator to use", possible_count_generator_names, key=f"node_{id}_count_generator")
            selected_count_generator = next(generator for generator in possible_count_generators if generator.name == selected_count_generator_name)
        with ncc2:
            count_arg_inputs = []
            if selected_count_generator is not None:
                for count_index, arg in enumerate(selected_count_generator.args):
                    if arg.type == GeneratorType.STRING:
                        count_arg = st.text_input(
                            label=arg.label, 
                            value = arg.default,
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            )
                    elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                        count_arg = st.number_input(
                            label= arg.label,
                            value= arg.default,
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            )
                    elif arg.type == GeneratorType.BOOL:
                        count_arg = st.radio(
                            label=arg.label,
                            index=arg.default,
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                        )
                    elif arg.type == GeneratorType.DATETIME:
                        count_arg = st.date_input(
                            label=arg.label,
                            value=datetime.datetime.fromisoformat(arg.default),
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}')
                    else:
                        count_arg = None
                    if count_arg is not None:
                        if count_index >= len(count_arg_inputs):
                            count_arg_inputs.append(count_arg)
                        else:
                            count_arg_inputs[count_index] = count_arg

        # Process disabled setting from earlier
        if disabled:
            # TODO: Also disable any relationships dependent on this node

            # Remove from mapping
            mapping = st.session_state[MAPPINGS]
            mapping_nodes = mapping.nodes
            if id in mapping_nodes:
                del mapping_nodes[id]
                mapping.nodes = mapping_nodes
                st.session_state[MAPPINGS] = mapping
            st.error(f'{caption} Node EXCLUDED from mapping')
        else:
            # Add to mapping
            mapping = st.session_state[MAPPINGS]
            nodes = mapping.nodes
            node_mapping = NodeMapping(
                id = id,
                caption = caption,
                position = position,
                labels = labels,
                properties=property_maps,
                count_generator=selected_count_generator,
                count_args=count_arg_inputs,
                key_property=selected_key_property,
                )
            nodes[id] = node_mapping
            mapping.nodes = nodes
            st.session_state[MAPPINGS] = mapping
            st.success(f'{caption } Node added to mapping')