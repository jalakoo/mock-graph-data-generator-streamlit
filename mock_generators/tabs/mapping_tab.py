import streamlit as st
from constants import *
import json
import logging
from widgets.node_row import nodes_row
from widgets.relationship_row import relationship_row
from widgets.property_row import property_row
import uuid
from models.node_mapping import NodeMapping
from models.relationship_mapping import RelationshipMapping
from models.mapping import Mapping
import sys

# Matching format from arrows.app json
def empty_node_dict():
    return {
        'id' : f'{str(uuid.uuid4())[:8]}',
        'labels' : [],
        'properties' : {
            "uuid":"string"
        },
        'caption' : None,
        'position':{
            'x': 0,
            'y': 0
        }
    }


def empty_relationship_dict():
    return {
        'id' : f'{str(uuid.uuid4())[:8]}',
        "type": None,
        "style": {},
        "properties": {},
        "fromId": "",
        "toId": ""
    }
    

# Callback processing from dynamically generated node and relationship configuration rows
def ignore_node(nid: str)-> bool:
    # Remove from mapping
    try:
        mapping = st.session_state[MAPPINGS]
        mapping_nodes = mapping.nodes
        if nid in mapping_nodes:
            del mapping_nodes[nid]
            mapping.nodes = mapping_nodes
            st.session_state[MAPPINGS] = mapping
        # st.success(f'Node {nid} EXCLUDED from mapping')
        return True
    except:
        st.error(f'Problem removing node {nid} from Mapping. ERROR: {sys.exc_info()[0]}')
        return False

# This function not working as expected
def delete_node(nid: str) -> bool:
    try:
        # Delete from mapping
        ignore_node(nid)
        # Delete from imported data
        if IMPORTED_NODES not in st.session_state:
            st.session_state[IMPORTED_NODES] = []
        nodes = st.session_state[IMPORTED_NODES]
        if nodes is not None and len(nodes) > 0:
            remaining_nodes = [node for node in nodes if node.get(nid) != nid]
            st.session_state[IMPORTED_NODES] = remaining_nodes
        else:
            st.session_state[IMPORTED_NODES] = []
        st.success(f'Node {nid} DELETED from imported list')
        return True
    except:
        logging.error(f'Problem deleting node {nid} from Imported Data. ERROR: {sys.exc_info()[0]}')
        # TODO: These returns won't be used, put st.errors and successes in here.
        st.error(f'Problem deleting node {nid} from Imported Data. ERROR: {sys.exc_info()[0]}')
        return False

def add_node(node: NodeMapping) -> bool:
    try:
        # Add to mapping
        mapping = st.session_state[MAPPINGS]
        nodes = mapping.nodes
        nodes[node.nid] = node
        mapping.nodes = nodes
        st.session_state[MAPPINGS] = mapping
        return True
    except:
        logging.error(f'Problem adding {node} to mapping. ERROR: {sys.exc_info()[0]}')
        return False

def ignore_relationship(rid: str)-> bool:
    try:
        mapping = st.session_state[MAPPINGS]
        mapping_relationships = mapping.relationships
        if rid in mapping_relationships:
            del mapping_relationships[rid]
            mapping.relationships = mapping_relationships
            st.session_state[MAPPINGS] = mapping
            return True
    except:
        logging.error(f'Problem excluding {type} relationship from mapping. ERROR: {sys.exc_info()[0]}')
        return False

def delete_relationship(rid: str) -> bool:
    try:
        # Delete the relationship from the mapping
        ignore_relationship(rid.rid)
        # Delete from imported list
        relationships = st.session_state[IMPORTED_RELATIONSHIPS]
        relationships = [relationship for relationship in relationships if relationship.rid != rid]
        st.session_state[IMPORTED_RELATIONSHIPS] = relationships
        logging.info(f'mapping_tab.py: Deleted relationship {rid} from imported list: {st.session_state[IMPORTED_RELATIONSHIPS]}')
        return True
    except:
        logging.error(f'Problem deleting relationship {rid}. ERROR: {sys.exc_info()[0]}')
        return False

def add_relationship(relationship: RelationshipMapping) -> bool:
    try:
        rid = relationship.rid
        mapping = st.session_state[MAPPINGS]
        relationships = mapping.relationships
        relationships[rid] = relationship
        mapping.relationships = relationships
        st.session_state[MAPPINGS] = mapping
    except:
        logging.error(f'Problem adding relationship {relationship.rid}. ERROR: {sys.exc_info()[0]}')
        return False
    return True

# Actual Tab UI and logic
def mapping_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/shuffle.gif")
    with col2:
        st.write("Create and edit mock data generation options. \n\nExpand options for each node or relationship to edit labels, property names, and assign generator functions that will create mock property data. NOTE: ALL Nodes require a unique key property name to be selected.\n\nWhen finished, proceed to the Generate Tab to generate mock data.")

    # Load the raw imported nodes and relationship data (these are not the node and relationship mapping objects created from this imported data)
    nodes = st.session_state[IMPORTED_NODES]
    relationships = st.session_state[IMPORTED_RELATIONSHIPS]
    if nodes is None:
        nodes = []
    if relationships is None:
        relationships = []

    st.markdown("--------")

    # Putting mapping status here is no good because of the top-down nature of streamlit updates, even when using session state. Mapping validaty state moved to the Generator tab which is further down the processing chain.


    st.subheader("**GLOBALS:**")
    num_global_properties = st.number_input("Number of Global Properties", min_value=0, value=0, help="Optional Properties added to ALL nodes and relationships. Will overwrite locally assigned Node or Relationship properties of the same name.")

    all_global_properties = []
    # if include_globals == True:
    for i in range(num_global_properties):
        global_property = property_row(
            type="global",
            pid = f'',
            index = i,
            properties = []
        )
        all_global_properties.append(global_property)

    # Nodes
    st.markdown("--------")
    # TODO: Add ability to add ALL NODES ONLY properties

    n1, n2 = st.columns([6,1])
    with n1:
        st.subheader("**NODES:**")
    with n2:

        num_nodes = st.number_input("Number:", min_value=1, value=len(relationships) if len(relationships) > 0 else 1, key="mapping_number_of_nodes", help="Adjust the number of nodes to generate")

        # TODO: Temp fix while the delete function not working
        if len(nodes) > num_nodes:
            # Remove unwanted nodes from mapping
            nodes_to_remove = nodes[num_nodes:]
            for remove in nodes_to_remove:
                ignore_node(remove.get("id"))
            # Remove nodes from import list
            nodes = nodes[:num_nodes]
        else:
            # Add nodes
            for i in range(len(nodes), num_nodes):
                nodes.append(empty_relationship_dict())

        # Disabling because delete function not working as expected
        # add_node_button = st.button(f"➕ Add Node", key="mapping_add_node_button")
        # if add_node_button:
        #     # Add an empty node dict to existing list
        #     nodes.append(empty_node_dict())
        #     st.experimental_rerun()

    # if len(nodes) == 0:
    #     # Auto insert an empty node bc that's going to be the first thing someone is going to need to do.
    #     nodes.append(empty_node_dict())

    for i in range(len(nodes)):
        if i >= len(nodes):
             #Should never be out of index, but just in case
            raise Exception(f"Node index {i} out of range of raw node dictionary list: {nodes}")
        node_dict = nodes[i]
        nodes_row(
            node_dict = node_dict,
            generators=st.session_state[GENERATORS], 
            # should_start_expanded=should_expand,
            additional_properties=all_global_properties,
            on_add=add_node,
            on_delete=delete_node,
            on_ignore= ignore_node
            )

    st.markdown("--------")
    r1, r2 = st.columns([6,1])
    with r1:
        st.subheader("**RELATIONSHIPS:**")
    # TODO: Add ability to add ALL RELATIONSHIPS ONLY properties
    with r2:
        num_relationships = st.number_input("Number:", min_value=0, value=len(relationships), key="mapping_number_of_relationships", help="Adjust the number of relationships to generate")

        # TODO: Temp fix while the delete function not working
        if len(relationships) > num_relationships:
            # Remove unwanted relationships from mapping
            relationships_to_remove = relationships[num_relationships:]
            for remove in relationships_to_remove:
                ignore_relationship(remove.get("id"))
            # Remove relationships from import list
            relationships = relationships[:num_relationships]
        else:
            # Add relationships
            for i in range(len(relationships), num_relationships):
                relationships.append(empty_relationship_dict())

        # Alt button option - but disabling because deleting not working as expected
        # add_relationship_button = st.button(f"➕ Add Relationship", key="mapping_add_relationship_button")
        # if add_relationship_button:
        #     # Add an empty node dictionary to the existing nodes list
        #     relationships.append(empty_relationship_dict())
        #     st.experimental_rerun()


    for i in range(len(relationships)):
        relationship_dict = None
        if i < len(relationships):
            relationship_dict = relationships[i]
        else:
            # Default new
            relationship_dict = empty_relationship_dict()

        relationship_row(
            relationship = relationship_dict,
            generators=st.session_state[GENERATORS],
            # should_start_expanded=should_expand,
            additional_properties=all_global_properties,
            on_add=add_relationship,
            on_delete=delete_relationship,
            on_ignore=ignore_relationship)

    st.markdown("--------")
    st.subheader("**MAPPING STATUS:**")
    # Mapping status - only really works at bottom of page here
    if MAPPINGS not in st.session_state:
        # Why hasn't mappings been preloaded by now?
        st.error(f'Mappings data was not preloaded')
    elif st.session_state[MAPPINGS] is None:
        st.error(f'Mappping option not valid for generation. Please configure options above.')
    elif st.session_state[MAPPINGS].is_empty() == True:
        st.error(f'No data currently mapped. Please configure above.')
    elif st.session_state[MAPPINGS].is_valid() == False:
        st.error(f'Mappping option not valid for generation. Please configure above.')
    else:
        st.success(f'Mappping options valid for generation. Can proceed to Generate Tab.')