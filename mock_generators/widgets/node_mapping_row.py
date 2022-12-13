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

# TODO: Should we track the index?
def node_mapping_row(
    node_mapping : NodeMapping,
    generators: dict[str,Generator],
    should_start_expanded: bool = False
    ):


    # Validation
    if generators is None or len(generators) == 0:
        logging.error(f'nodes_mapping_row.py: No generators received for node {node_mapping.caption}')
        return None
        
    id = node_mapping.id
    # Work around to (eventually) update node caption in expander when new primary label updated by
    # saved_node = st.session_state[MAPPINGS].nodes.get(id) 
    # if saved_node is not None:
    #     caption = saved_node.caption
    #     labels = saved_node.labels

    # Create expandable list item for each node

    # Caption of node may be changed by user, so we'll hook into Streamlit's sessions to update the expander text when that happens.

    # Create an expander view for each node
    with st.expander(f'{node_mapping.caption}', expanded=should_start_expanded):
        # Select count of nodes to generate
        st.markdown('---')
        st.write(f'Number of {node_mapping.caption} records to generate')
        # possible_count_generators = generators_filtered([GeneratorType.INT])
        if generators is None:
            st.error("No generators passed to node row.")
            st.stop()
        
        # possible_count_generators = [generator for _, generator in generators.items() if generator.type in [GeneratorType.INT]]
        possible_count_generators = [generator for generator in generators.values()]

        if possible_count_generators is None or len(possible_count_generators) == 0:
            st.error(f"No possible generators found for type INT from generators arg: {generators}.")
            st.stop()
        possible_count_generator_names = [generator.name for generator in possible_count_generators]
        possible_count_generator_names.sort(reverse=False)
        if possible_count_generator_names is None or len(possible_count_generator_names) == 0:
            st.error(f"No possible generator names found for type INT from possible_count_generator_names: {possible_count_generator_names}.")
            st.stop()

        ncc1, ncc2 = st.columns(2)

        with ncc1:
            selected_count_generator_name = st.selectbox("Int Generator to use", possible_count_generator_names, key=f"node_mapping_{id}_count_generator")
            possible_selected_count_generators =[generator for generator in possible_count_generators if generator.name == selected_count_generator_name]
            if len(possible_selected_count_generators) == 0:
                st.error(f'Generator "{selected_count_generator_name}" not found.')
                st.stop()
            else:
                selected_count_generator = possible_selected_count_generators[0]
            # selected_count_generator = next(generator for generator in possible_count_generators if generator.name == selected_count_generator_name)
        with ncc2:
            count_arg_inputs = []
            if selected_count_generator is not None:
                for count_index, arg in enumerate(selected_count_generator.args):
                    if arg.type == GeneratorType.STRING:
                        count_arg = st.text_input(
                            label=arg.label, 
                            value = arg.default,
                            key = f'node_mapping_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            )
                    elif arg.type == GeneratorType.INT or arg.type == GeneratorType.FLOAT:
                        count_arg = st.number_input(
                            label= arg.label,
                            value= arg.default,
                            key = f'node_mapping_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                            )
                    elif arg.type == GeneratorType.BOOL:
                        count_arg = st.radio(
                            label=arg.label,
                            index=arg.default,
                            key = f'node_mapping_{id}_count_generator_{selected_count_generator.id}_{arg.label}'
                        )
                    elif arg.type == GeneratorType.DATETIME:
                        count_arg = st.date_input(
                            label=arg.label,
                            value=datetime.datetime.fromisoformat(arg.default),
                            key = f'node_mapping_{id}_count_generator_{selected_count_generator.id}_{arg.label}')
                    else:
                        count_arg = None
                    if count_arg is not None:
                        if count_index >= len(count_arg_inputs):
                            count_arg_inputs.append(count_arg)
                        else:
                            count_arg_inputs[count_index] = count_arg


        # Update the node mapping

        node_mapping.count_generator = selected_count_generator
        node_mapping.count_args = count_arg_inputs

        # Process disabled setting from earlier
        # if disabled:
        #     # TODO: Also disable any relationships dependent on this node

        #     # Remove from mapping
        #     mapping = st.session_state[MAPPINGS]
        #     mapping_nodes = mapping.nodes
        #     if id in mapping_nodes:
        #         del mapping_nodes[id]
        #         mapping.nodes = mapping_nodes
        #         st.session_state[MAPPINGS] = mapping
        #     st.error(f'{caption} Node EXCLUDED from mapping')
        # else:
        # Add to mapping
        mapping = st.session_state[MAPPINGS]
        nodes = mapping.nodes
        # node_mapping = NodeMapping(
        #     id = id,
        #     caption = caption,
        #     position = position,
        #     labels = labels,
        #     properties=property_maps,
        #     count_generator=selected_count_generator,
        #     count_args=count_arg_inputs,
        #     key_property=selected_key_property,
        #     )
        nodes[id] = node_mapping
        mapping.nodes = nodes
        st.session_state[MAPPINGS] = mapping
        st.success(f'{node_mapping.caption } Node updated in mapping')