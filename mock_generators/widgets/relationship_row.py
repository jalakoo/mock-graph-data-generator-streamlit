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
from widgets.arguments import generator_arguments
from widgets.generator_selector import generator_selector
from collections.abc import Callable

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
    possible_nodes = [node for _, node in nodes.items() if node.nid == id]
    if len(possible_nodes) == 0:
        return NodeMapping.empty()
    else:
        return possible_nodes[0]

def relationship_row(
        relationship: dict,
        should_start_expanded: bool = False,
        generators = dict[str,Generator],
        additional_properties: list[PropertyMapping] = [],
        on_add: Callable[[RelationshipMapping], bool] = None,
        on_delete: Callable[[RelationshipMapping], bool] = None,
        on_ignore: Callable[[str], bool] = None,
    ):

    if relationship is not None:
        id = relationship.get("id", str(uuid.uuid4())[:8])
        type = relationship.get("type",None)
        fromId = relationship.get("fromId")
        toId = relationship.get("toId")
        if 'properties' in relationship:
            properties = [(k,v) for k,v in relationship.get("properties").items()]
        else:
            properties = []
    else:
        raise Exception(f'relationship_row: No relationship data received')

    # Use existing mapped relationship if it exists. Has to be called after the relationship dict is processed for the id
    mapped_relationships = st.session_state[MAPPINGS].relationships
    if id in mapped_relationships.keys():
        mapped_relationship = mapped_relationships[id]
        if mapped_relationship is not None:
            type = mapped_relationship.type
            fromId = mapped_relationship.from_node.nid
            toId = mapped_relationship.to_node.nid

    # Validation
    if generators is None or len(generators) == 0:
        logging.error(f'relationship_row: No generators received for relationship {type}')
        return


    from_node = NodeMapping.empty()
    to_node = NodeMapping.empty()
    if fromId is not None:
        from_node = node_from_id(fromId)
    if toId is not None:
        to_node = node_from_id(toId) 
    should_enable = True
       
    expander_text = f"(:{from_node.caption})-[:{type if type is not None else  '<new_relationship>'}]->(:{to_node.caption})"

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
            # TODO: Notice that change may not be reflected until refresh

        with r2:
            # Relationship type
            new_type = st.text_input("Type", value=type, key=f"relationship_{id}_type", help="Change the Relationship type. Change will be reflected in the Raw Mapping Data in the Generate Tab")
            if new_type != type:
                type = new_type
                st.info(f"Relationship type changed to {type}. Change not reflected above until page refresh")
            if new_type is None or new_type == "":
                st.error("Relationship type cannot be empty")
 
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
            if disabled == True:
                should_enable = False
                if on_ignore is not None:
                    on_ignore(id)
            # Not currently working as expected
            # delete = st.button("Delete relationship", key=f"relationship_{id}_delete")
            # if delete and on_delete is not None:
            #     on_delete(id)

        r_tab1, r_tab2, r_tab3 = st.tabs(["Properties","Count", "To Conditions"])

        with r_tab1:
            # Relationship properties
            num_properties = st.number_input("Number of properties", min_value=0, value=len(properties), key=f"relationship_{id}_number_of_properties")
            property_maps = {}
            
            for i in range(num_properties):
                # Create a new propertyMapping for storing user selections

                new_property_map = property_row(
                    type="relationship",
                    pid=id,
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



        if fromNode is None:
            return
        if toNode is None:
            return
        if type is None:
            return
        if selected_count_generator is None:
            return
        if selected_assignment_generator is None:
            return

        if should_enable:
            relationship_mapping = RelationshipMapping(
                rid=id,
                type=type,
                properties=property_maps,
                from_node = fromNode,
                to_node = toNode,
                count_generator = selected_count_generator,
                count_args = count_arg_inputs,
                assignment_generator=selected_assignment_generator,
                assignment_args=assignment_arg_inputs
            )
            # Auto add to mapping
            if on_add is not None:
                if on_add(relationship_mapping) == True:
                    st.success(f'{type} relationship INCLUDED in mapping')
                    # Error display will be handled by callback function
        else:
            st.error(f'{type} relationship EXCLUDED from mapping')