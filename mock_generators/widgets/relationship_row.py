import streamlit as st
from constants import *
import uuid
from models.property_mapping import PropertyMapping
from models.generator import Generator, GeneratorType
from models.relationship_mapping import RelationshipMapping
from models.node_mapping import NodeMapping
import datetime
import logging
from widgets.property_row import property_row
# from widgets.default_state import load_state
from widgets.arguments import generator_arguments
from widgets.generator_selector import generator_selector

# load_state()

# def generators_filtered(
#     generators:list[Generator],
#     byTypes: list[GeneratorType]
#     ) -> list[Generator]:

#     return [generator for _, generator in generators.items() if generator.type in byTypes]

def _node_uid_from(caption: str)-> str:
    nodes = st.session_state[MAPPINGS].nodes
    options = [uid for uid, node in nodes.items() if node.caption == caption]
    if len(options) == 0:
        logging.error(f'No node found with caption {caption} (possibly disabled)')
        return None
    else:
        return options[0]

def _all_node_captions()-> list[str]:
    nodes = st.session_state[MAPPINGS].nodes
    return [node.caption for _, node in nodes.items()]

def _node_index_from(uid: str)-> int:
    nodes = st.session_state[MAPPINGS].nodes
    if uid in nodes.keys():
        return list(nodes.keys()).index(uid)
    # If the node is not found, return index 0 as this is used by a UI widget
    return -1

def node_from_id(id: str) -> NodeMapping:
    nodes = st.session_state[MAPPINGS].nodes
    return [node for _, node in nodes.items() if node.id == id][0]

def relationship_row(
        relationship: dict,
        should_start_expanded: bool = False,
        generators = dict[str,Generator],
        additional_properties: list[PropertyMapping] = []
    ):

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

    # relationship = st.session_state[IMPORTED_RELATIONSHIPS][index]

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

    # Validation
    if generators is None or len(generators) == 0:
        logging.error(f'relationship_row: No generators received for relationship {type}')
        return

    # As a work around to (eventually) update the expander title when type changed by user.
    saved_relationship = st.session_state[MAPPINGS].relationships.get(id) 
    if saved_relationship is not None:
        type = saved_relationship.type
        
    expander_text = f"(:{node_from_id(fromId).caption})-[:{type}]->(:{node_from_id(toId).caption})"
    with st.expander(expander_text, expanded=should_start_expanded):

        # # Relationship source and target nodes
        r1, r2, r3, r4 = st.columns([2, 2, 2, 1])

        with r1:
            # Relationship from
            fromId_index = _node_index_from(fromId)
            if fromId_index == -1:
                st.error(f'Node with id {fromId} disabled or missing')
                fromId_index = 0
            new_from_node_caption = st.selectbox("From Node", index=fromId_index, options=_all_node_captions(), key=f"relationship_{id}_fromId", help="A random node of this type will be selected as the source of the relationship")
            new_fromId = _node_uid_from(new_from_node_caption)
            fromNode = node_from_id(new_fromId)

        with r2:
            # Relationship type
            new_type = st.text_input("Type", value=type, key=f"relationship_{id}_type", help="Change the Relationship type. Change will be reflected in the Raw Mapping Data in the Generate Tab")
            if new_type != type:
                type = new_type
                st.info(f"Relationship type changed to {type}. Change not reflected above until page refresh")
 
        with r3:
            # Relationship to
            toId_index = _node_index_from(toId)
            if toId_index == -1:
                st.error(f'Node with id {toId} disabled or missing')
                toId_index = 0
            new_to_node_caption = st.selectbox("To Node", index=toId_index, options=_all_node_captions(), key=f"relationship_{id}_toId", help="A random node of this type will be selected as the target of the relationship")
            new_toId = _node_uid_from(new_to_node_caption)
            toNode = node_from_id(new_toId)
        with r4:
            st.write('Options')
            disabled = st.checkbox("Exclude/ignore relationship", value=False, key=f"relationship_{id}_enabled")

        r_tab1, r_tab2, r_tab3 = st.tabs(["Properties","Count", "To Conditions"])

        with r_tab1:
            # Relationship properties
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

        # with r_tab2:
            # Filter from node sources for particular property values
            # st.write(f'<filter_from_node_options_tbd>')
        with r_tab2:
            # Count Generator Options
            r1, r2, r3 = st.columns([1, 1, 1])

            with r1:
                # Select count generator
                selected_count_generator = generator_selector(
                    label="Using Generator",
                    types=[GeneratorType.INT],
                    generators=generators,
                    key=f"relationship_{id}_count_generator",
                )
 
            with r2:
                # Optional generator args
                count_arg_inputs = generator_arguments(selected_count_generator, f"relationship_{id}_count_generator")
 
            with r3:
                # Display sample output
                st.write("Sample value")
                if selected_count_generator is not None:
                    st.write(selected_count_generator.generate(count_arg_inputs))

        with r_tab3:
            # User decides how to assign relationships to target nodes

            ra1, ra2 = st.columns(2)

            with ra1:
                selected_assignment_generator = generator_selector(
                    label="Assignment Generator",
                    generators=generators,
                    types = [GeneratorType.ASSIGNMENT],
                    key=f'relationship_{id}_assignment_generator'
                )
            with ra2:
                assignment_arg_inputs = generator_arguments(selected_assignment_generator, f"relationship_{id}_assignment_generator")
            # 1. Randomly assign relationships to target nodes
            # 1a. Randomly assign relationships to target nodes, but ensure that each target node has at least one relationship
            # 1b. Randomly assign relationships to target nodes, but ensure that each target node has at MAX of x relationships
            # 2. Sort target nodes by property value and assign relationships to target nodes in order
            # 3. Sort target nodes by property value and assign relationships to target nodes in reverse order


        # Load any additional properties that were passed in
        if additional_properties != None and len(additional_properties) > 0:
            for additional_property in additional_properties:
                property_maps[additional_property.name] = additional_property

        # Effect enable/disable options
        if disabled:
            # Remove from mapping
            mapping = st.session_state[MAPPINGS]
            mapping_relationships = mapping.relationships
            if id in mapping_relationships:
                del mapping_relationships[id]
                mapping.relationships = mapping_relationships
                st.session_state[MAPPINGS] = mapping
            st.error(f'{type} relationship EXCLUDED from mapping')
        else:
            mapping = st.session_state[MAPPINGS]
            relationships = mapping.relationships
            relationship_mapping = RelationshipMapping(
                id=id,
                type=type,
                properties=property_maps,
                from_node = fromNode,
                to_node = toNode,
                count_generator = selected_count_generator,
                count_args = count_arg_inputs,
                assignment_generator=selected_assignment_generator,
                assignment_args=assignment_arg_inputs
            )
            relationships[id] = relationship_mapping
            mapping.relationships = relationships
            st.session_state[MAPPINGS] = mapping
            st.success(f'{type} relationship added to mapping')