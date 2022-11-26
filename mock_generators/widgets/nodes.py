import streamlit as st
from constants import *
from widgets.property import property_row
from models.generator import Generator, GeneratorType
import uuid
import datetime
import logging

def generators_filtered(byType: GeneratorType) -> list[Generator]:
    generators = st.session_state[GENERATORS]
    return [generator for _, generator in generators.items() if generator.type == byType]

# def generator_by_name(generators: list[Generator])->Generator:


def nodes_row(
    node: dict
    ):

    #  Sample dict from arrows.app
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
        properties = []
        selected_labels = []
    else:
        id = node.get("id")
        labels = node.get("labels")
        labels.append(node.get("caption"))
        properties = [(k,v) for k,v in node.get("properties").items()]
        selected_labels = labels

    with st.expander(f"NODE {id} - {labels}"):
        st.markdown('---')

        # Adjust number of labels
        num_labels = st.number_input("Number of labels", min_value=1, value=len(labels), key=f"node_{id}_num_labels")
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
        num_properties = st.number_input("Number of properties", value = len(properties), key= f'node_{id}_num_properties')
        for i in range(num_properties):
            pc1, pc2, pc3, pc4 = st.columns(4)
            with pc1:
                existing_name = ""
                if i < len(properties):
                    # Get key of property
                    existing_name = properties[i][0] 
                name = st.text_input("Name",value=existing_name, key=f"node_{id}_property_{i}_name")
            with pc2:
                type_string = st.selectbox("Type", ["String", "Bool", "Int", "Float","Datetime"], key=f"node_{id}_property_{i}_type")
                type = GeneratorType.type_from_string(type_string)
            with pc3:
                possible_generators = generators_filtered(type)
                possible_generator_names = [generator.name for generator in possible_generators]
                selected_generator_name = st.selectbox("Generator", possible_generator_names, key=f"node_{id}_property_{i}_generator")
            with pc4:
                arg_inputs = []
                selected_generator = next(generator for generator in possible_generators if generator.name == selected_generator_name)
                logging.info(f'node_row: selected generator: {selected_generator}')
                if selected_generator is not None and selected_generator.args is not None:
                    for arg in selected_generator.args:
                        if arg.type == GeneratorType.STRING:
                            arg_inputs.append(st.text_input(
                                label=arg.label, 
                                value = arg.default,
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                ))
                        if arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                            arg_inputs.append(st.number_input(
                                label= arg.label,
                                value= arg.default,
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                                ))
                        if arg.type == GeneratorType.BOOL:
                            arg_inputs.append(st.radio(
                                label=arg.label,
                                index=arg.default,
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                            ))
                        if arg.type == GeneratorType.DATETIME:
                            arg_inputs.append(st.date_input(
                                label=arg.label,
                                value=datetime.datetime.fromisoformat(arg.default),
                                key = f'node_{id}_property_{i}_generator_{selected_generator.id}_{arg.label}'
                            ))
        st.markdown('---')
        num_select_nodes = st.number_input("Count", value = 0, key=f"node_{id}_num_nodes")