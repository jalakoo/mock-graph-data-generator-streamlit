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
from widgets.default_state import load_state
from widgets.arguments import generator_arguments
from widgets.generator_selector import generator_selector

def nodes_row(
    node_dict : dict,
    generators: dict[str,Generator],
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

    # Extract relevant data from node dict
    if node_dict is not None:
        # Load node data from an imported dict
        id = node_dict.get("id")

        # Otherwise, use the imported dict info
        labels = node_dict.get("labels", [])
        position = {
            "x": node_dict.get("position", {}).get("x", 0),
            "y": node_dict.get("position", {}).get("y", 0)
        }
        caption = node_dict.get("caption", "")
        properties = [(k,v) for k,v in node_dict.get("properties").items()]
        selected_labels = labels
    else:
        # Or crash - default data, which needs to contain enough differentiating content from other nodes, should have been passed in by calling code
        raise Exception(f'nodes_row.py: No node data received')

    # Node might have already been mapped, if so, use that
    mapped_nodes = st.session_state[MAPPINGS].nodes
    if id in mapped_nodes.keys():
        node = mapped_nodes[id]
        labels = node.labels
        position = node.position
        caption = node.caption
        # NodeMapping properties are PropertyMapping objects instead of the dict found in the imported node dict, so we're not going to convert these back as streamlit is already holding onto the new property rows through soft page refreshes
        # properties = node.properties
        # selected_labels not retained in node mapping

    # Validation
    if generators is None or len(generators) == 0:
        logging.error(f'nodes_row.py: No generators received for node {caption}')
        return None

    # Create expandable list item for each node

    # Caption of node may be changed by user, so we'll hook into Streamlit's sessions to update the expander text when that happens.

    # Create an expander view for each node
    with st.expander(f'{caption}', expanded=should_start_expanded):

        node_tab_1, node_tab_2, node_tab_3 = st.tabs(["Labels", "Properties", "Count"])

        with node_tab_1:
            # Adjust node label(s)
            labels1, labels2, labels3, labels4 = st.columns(4)

            # Display/edit Caption
            with labels1:
                new_caption = st.text_input(
                f"Primary Label", 
                value = caption,
                key=f"node_{id}_primary_label",
                help="The primary label for this node. Changes will be reflected here and in Raw Mapping Data (but not the disclosure section title)")
                if new_caption != caption:
                    old_caption = str(caption)
                    caption = new_caption
                    st.info(f"{old_caption} changed to {caption}. Change not reflected above until page refresh")


            # Adjust number of labels
            with labels2:
                num_labels = st.number_input("Additional labels", min_value=0, value=len(labels), key=f"node_{id}_num_labels", help="Nodes may have more than one label. Select the number of additional labels to add")
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

            # with labels3:
            #     initial_num_properties = len(properties)
            #     # All nodes should have at least one property
            #     # Otherwise we're just generating a bunch of empty nodes
            #     # which doesn't require a mock data generator to do. But
            #     # whatever, maybe someone needs a few label only nodes
            #     num_properties = st.number_input("Properties", value = initial_num_properties, min_value=0, key= f'node_{id}_num_properties', help="Nodes typically have one or more properties. Select the number of properties for this node.")

            with labels3:
                st.write('Options')
                disabled = st.checkbox("Exclude/ignore node", value=False, key=f"node_{id}_disabled")


        with node_tab_2:
            # Adjust properties
            initial_num_properties = len(properties)
            # All nodes should have at least one property
            # Otherwise we're just generating a bunch of empty nodes
            # which doesn't require a mock data generator to do. But
            # whatever, maybe someone needs a few label only nodes
            num_properties = st.number_input("Properties", value = initial_num_properties, min_value=0, key= f'node_{id}_num_properties', help="Nodes typically have one or more properties. Select the number of properties for this node.")

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
                    properties= properties
                )

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
            if len(property_maps.keys()) == 0:
                st.info(f'Add properties before selecting a key property for node {caption}')
                selected_key_property = None
            elif key_property_name not in property_maps:
                st.error(f'Property "{key_property_name}" does not exist in properties for node {caption}')
                selected_key_property = None
            else:
                selected_key_property = property_maps[key_property_name]
        
        with node_tab_3:

            # Select count of nodes to generate
            st.write(f'Number of {caption} records to generate')
            # possible_count_generators = generators_filtered([GeneratorType.INT])
            if generators is None:
                st.error("No generators passed to node row.")
                st.stop()

            ncc1, ncc2 = st.columns(2)

            with ncc1:
                selected_count_generator = generator_selector(
                    label="Int Generator to use",
                    generators=generators,
                    types=[GeneratorType.INT],
                    key=f"node_{id}_test_count_generator",
                )

            with ncc2:
                count_arg_inputs = generator_arguments(selected_count_generator, f'node_{id}_count_generator')


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