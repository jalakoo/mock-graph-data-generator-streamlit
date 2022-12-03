import streamlit as st
from constants import *
import uuid
from models.property_mapping import PropertyMapping
from models.generator import Generator, GeneratorType
from models.relationship_mapping import RelationshipMapping
import datetime
import logging
from widgets.property_row import property_row

def generators_filtered(byTypes: list[GeneratorType]) -> list[Generator]:
    generators: list[Generator] = st.session_state[GENERATORS]
    return [generator for _, generator in generators.items() if generator.type in byTypes]

def _node_uid_from(caption: str)-> str:
    nodes = st.session_state[MAPPINGS].nodes
    return [uid for uid, node in nodes.items() if node.caption == caption][0]

def _node_caption_from(uid: str)-> str:
    nodes = st.session_state[MAPPINGS].nodes
    return nodes[uid].caption

def _all_node_captions()-> list[str]:
    nodes = st.session_state[MAPPINGS].nodes
    return [node.caption for _, node in nodes.items()]

def _all_node_ids()-> list[str]:
    nodes = st.session_state[MAPPINGS].nodes
    return [uid for uid, _ in nodes.items()]

def _node_index_from(uid: str)-> int:
    nodes = st.session_state[MAPPINGS].nodes
    return list(nodes.keys()).index(uid)

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

        # Relationship source and target nodes
        st.markdown('---')
        st.write("Number of relationships to generate")
        r1, r2, r3, r4, r5 = st.columns([1, 1, 2, 1,1])

        with r1:
            # Relationship from
            fromId_index = _node_index_from(fromId)
            new_from_node_caption = st.selectbox("From Node", index=fromId_index, options=_all_node_captions(), key=f"relationship_{id}_fromId", help="A random node of this type will be selected as the source of the relationship")
            # new_fromId = st.text_input("From Node", value=fromId, key=f"relationship_{id}_fromId")
            new_fromId = _node_uid_from(new_from_node_caption)
            if new_fromId != fromId:
                fromId = new_fromId
        with r2:
            # Select count generator
            possible_count_generators = generators_filtered([GeneratorType.INT])
            possible_count_generator_names = [generator.name for generator in possible_count_generators]
            selected_count_generator_name = st.selectbox("Using Generator", possible_count_generator_names, key=f"relationship_{id}_count_generator", help="This integer generator will be used for generating the number of relationships from source node to target node. For example, an output of 5 would create 5 relationships between the 'from node' to the 'to node'")
            selected_count_generator = next(generator for generator in possible_count_generators if generator.name == selected_count_generator_name)
        with r3:
            # Optional generator args
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
        with r4:
            # Display sample output
            st.write("Sample # of relationships to >")
            if selected_count_generator is not None:
                st.write(selected_count_generator.generate(count_arg_inputs))

        with r5:
            # Relationship to
            toId_index = _node_index_from(toId)
            new_to_node_caption = st.selectbox("To Node", index=toId_index, options=_all_node_captions(), key=f"relationship_{id}_toId", help="A random node of this type will be selected as the target of the relationship")
            # new_toId = st.text_input("To Node", value=toId, key=f"relationship_{id}_toId")
            new_toId = _node_uid_from(new_to_node_caption)
            if new_toId != toId:
                toId = new_toId

        # Relationship properties
        st.markdown('---')
        num_properties = st.number_input("Number of properties", min_value=0, value=len(properties), key=f"relationship_{id}_number_of_properties")

        property_maps = {}
        
        for i in range(num_properties):
            # Create a new propertyMapping for storing user selections

            new_property_map = property_row(
                type="relationship",
                id=id,
                index=i,
                properties=properties
            )

            if new_property_map.name in property_maps:
                st.error(f'Property "{new_property_map.name}" already exists')
            else:
                property_maps[new_property_map.name] = new_property_map
        
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
          
        # # Randomization Mode
        # st.markdown('---')
        # st.selectbox(f'Relationship Randomization Mode', options=['Pure Random', 'Random Once Per Node Ongoing', 'Random Once Per Node Max'], key=f"relationship_{id}_randomization_mode",help='Relationships are randomly linked between generated node values. Optionally change how this is done. For example: pure random, random once per node max, etc.')