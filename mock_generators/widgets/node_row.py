import streamlit as st
from constants import *
from widgets.property import property_row
from models.generator import Generator, GeneratorType
from models.mapping import Mapping, NodeMapping, PropertyMapping
import uuid
import datetime
import logging

def generators_filtered(byType: GeneratorType) -> list[Generator]:
    generators = st.session_state[GENERATORS]
    return [generator for _, generator in generators.items() if generator.type == byType]

def nodes_row(
    node: dict
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

    # Optionally prelude options from an import
    if node is None:
        id = str(uuid.uuid4())[:8]
        labels = ["<add_label>"]
        caption = ""
        properties = []
        selected_labels = []
    else:
        id = node.get("id")
        labels = node.get("labels", [])
        caption = node.get("caption", "")
        properties = [(k,v) for k,v in node.get("properties").items()]
        selected_labels = labels

    with st.expander(f"NODE {id} - {caption}"):
        st.markdown('---')

        # Caption
        new_caption = st.text_input(
        f"Primary Label", 
        value = caption,
        key=f"node_{id}_primary_label")
        if new_caption != caption:
            caption = new_caption

        # Adjust number of labels
        num_labels = st.number_input("Number of Additional labels", min_value=0, value=len(labels), key=f"node_{id}_num_labels")
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

        st.markdown('---')

        # Adjust properties + assign generators
        num_properties = st.number_input("Number of properties", value = len(properties), min_value=0, key= f'node_{id}_num_properties')
        property_map = None
        property_maps = []
        for i in range(num_properties):
            property_map = PropertyMapping(id=f'node_{id}_property_{i}')
            pc1, pc2, pc3, pc4, pc5 = st.columns(5)
            with pc1:
                existing_name = ""
                if i < len(properties):
                    # Get key of property
                    existing_name = properties[i][0] 
                name = st.text_input("Property Name",value=existing_name, key=f"node_{id}_property_{i}_name")
                property_map.name = name
            with pc2:
                type_string = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"node_{id}_property_{i}_type")
                type = GeneratorType.type_from_string(type_string)
                property_map.type = type
            with pc3:
                possible_generators = generators_filtered(type)
                possible_generator_names = [generator.name for generator in possible_generators]
                selected_generator_name = st.selectbox("Generator", possible_generator_names, key=f"node_{id}_property_{i}_generator")
                selected_generator = next(generator for generator in possible_generators if generator.name == selected_generator_name)
                property_map.generator = selected_generator
            with pc4:
                arg_inputs = []
                # logging.info(f'node_row: selected generator: {selected_generator}')
                if selected_generator is not None and selected_generator.args is not None:

                    # Change to enumarate to get index
                    for index, arg in enumerate(selected_generator.args):
                        if arg.type == GeneratorType.STRING:
                            arg_input = st.text_input(
                                label=arg.label, 
                                value = arg.default,
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                )
                        elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                            arg_input = st.number_input(
                                label= arg.label,
                                value= arg.default,
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                )
                        elif arg.type == GeneratorType.BOOL:
                            arg_input = st.radio(
                                label=arg.label,
                                index=arg.default,
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                            )
                            # arg_inputs.append()
                        elif arg.type == GeneratorType.DATETIME:
                            arg_input = st.date_input(
                                label=arg.label,
                                value=datetime.datetime.fromisoformat(arg.default),
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}')

                        if index > len(property_map.args):
                            property_map.args.append(arg_input)
                        else:
                            property_map.args[index] = arg_input
                        arg_inputs.append(arg_input)
                        property_maps.append(property_map)
                        
            with pc5:
                module = __import__(selected_generator.import_url(), fromlist=['generate'])
                # logging.info(f'arg_inputs: {arg_inputs}')
                result = module.generate(arg_inputs)
                st.write(f'Sample')
                st.text(f'{result}')

        st.markdown('---')
        st.write('Number of these nodes to generate')
        possible_count_generators = generators_filtered(GeneratorType.INT)
        possible_count_generator_names = [generator.name for generator in possible_count_generators]

        ncc1, ncc2, ncc3 = st.columns(3)

        with ncc1:
            selected_count_generator_name = st.selectbox("Int Generator to use", possible_count_generator_names, key=f"node_{id}_count_generator")
            selected_count_generator = next(generator for generator in possible_count_generators if generator.name == selected_count_generator_name)
        with ncc2:
            count_arg_inputs = []
            if selected_count_generator is not None:
                for arg in selected_count_generator.args:
                    if arg.type == GeneratorType.STRING:
                        count_arg_inputs.append(st.text_input(
                            label=arg.label, 
                            value = arg.default,
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            ))
                    if arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                        count_arg_inputs.append(st.number_input(
                            label= arg.label,
                            value= arg.default,
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            ))
                    if arg.type == GeneratorType.BOOL:
                        count_arg_inputs.append(st.radio(
                            label=arg.label,
                            index=arg.default,
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                        ))
                    if arg.type == GeneratorType.DATETIME:
                        count_arg_inputs.append(st.date_input(
                            label=arg.label,
                            value=datetime.datetime.fromisoformat(arg.default),
                            key = f'node_{id}_count_generator_{selected_count_generator.id}_{arg.label}'))
        with ncc3:
            enabled = st.checkbox("Generate Data for this node", value=False, key=f"node_{id}_enabled")
            if enabled:
                # Add to mapping
                mapping = st.session_state[MAPPINGS]
                nodes = mapping.nodes
                # logging.info(f'nodes: {nodes}')
                node_mapping = NodeMapping(
                    id = id,
                    position = node.get("position", {"x": 0, "y": 0}),
                    labels = labels,
                    properties=property_maps,
                    count_generator=selected_count_generator,
                    count_generator_args=count_arg_inputs,)
                nodes[id] = node_mapping
                mapping.nodes = nodes
                st.session_state[MAPPINGS] = mapping
                st.info(f'Nodes added to mapping')
            else:
                # Remove from mapping
                mapping = st.session_state[MAPPINGS]
                mapping_nodes = mapping.nodes
                if id in mapping_nodes:
                    del mapping_nodes[id]
                    mapping.nodes = mapping_nodes
                    st.session_state[MAPPINGS] = mapping
                st.warning(f'Nodes EXCLUDED from mapping')
          