import streamlit as st
import graph_data_generator as gdg
from neo4j_uploader import (
    Neo4jConfig,
    upload,
    start_logging,
    UploadResult,
    convert_legacy_node_records,
    convert_legacy_relationship_records,
    batch_upload_generator,
)
from typing import Callable

import json
import logging

# Limit default Neo4j verbosity level
logging.getLogger("neo4j.io").setLevel(logging.INFO)
logging.getLogger("neo4j.pool").setLevel(logging.INFO)
logging.getLogger("neo4j_uploader").setLevel(logging.INFO)


def export_ui():

    txt = st.session_state.get("JSON_CONFIG", None)
    if txt is None:
        st.error("Add JSON config to generate data")
        return

    # TODO: Add a generate data button here?

    # Generate data
    mapping = gdg.generate_mapping(txt)
    data = gdg.generate_dictionaries(mapping)

    with st.expander("Generated Data"):
        pretty = json.dumps(data, indent=4, default=str)
        st.code(pretty)

    # Display node and relationship counts
    all_nodes = data.get("nodes", None)
    nodes_count = 0
    for _, nodes_list in all_nodes.items():
        nodes_count += len(nodes_list)

    all_relationships = data.get("relationships", None)
    relationships_count = 0
    for _, relationships_list in all_relationships.items():
        relationships_count += len(relationships_list)

    st.write(f"{nodes_count} Nodes and {relationships_count} Relationships generated")

    st.markdown("**③ EXPORT**")

    c1, c2 = st.columns([1, 1])
    with c1:
        with st.expander("Download .zip file"):

            st.markdown(
                "That can be uploaded into [Neo4j's Data Importer](https://neo4j.com/docs/data-importer/current/)"
            )

            # Create .zip file for data-importer
            filename = st.text_input(
                "Name of file",
                value="mock_data",
                help="Name of file to be used for the.zip file. Ignored if pushing directly to a Neo4j database instance.",
            )

            def on_download():
                st.session_state["DOWNLOADING"] == True

            try:
                zip = gdg.package(mapping)
                if zip is None:
                    st.warning(
                        "Unexpected problem generating file. Try an alternate JSON input"
                    )
                else:
                    st.download_button(
                        label="Download .zip file",
                        data=zip,
                        file_name=f"{filename}.zip",
                        mime="text/plain",
                        on_click=on_download,
                    )
            except Exception as e:
                st.error(e)

    with c2:
        with st.expander("Upload to Neo4j"):

            uri = st.text_input(
                f"Neo4j URI",
                value=st.session_state["NEO4J_URI"],
                placeholder="neo4j+s//92bd05dc.databases.neo4j.io",
                help="URI for your Aura Neo4j instance",
            )

            user = st.text_input(
                f"Neo4j USER", value=st.session_state["NEO4J_USER"], placeholder="neo4j"
            )

            password = st.text_input(
                f"Neo4j PASSWORD",
                type="password",
                value=st.session_state["NEO4J_PASSWORD"],
            )

            should_overwrite = st.toggle(
                "Reset DB",
                value=True,
                help="All data in target database be deleted before upload if enabled. Default Enabled. Note: Large databases may take a long time to reset.",
            )

            if st.button(
                "Upload to Neo4j", help="Upload generated data to a Neo4j instance"
            ):
                # Upload credentials check
                if uri is None or user is None or password is None:
                    st.error(
                        "Please specify the Neo4j instance credentials in the Configuration tab"
                    )
                    return

                # Execute upload
                else:

                    # Using st.spinner to show progress
                    # with st.spinner("Uploading..."):
                    #     result = upload(
                    #         neo4j_creds=(uri, user, password),
                    #         data=data,
                    #         should_overwrite=should_overwrite,
                    #     )
                    #     if result is None:
                    #         st.error(f"Unexpected result: {result}")
                    #     else:
                    #         if result.was_successful == False:
                    #             st.error(f"Upload Errors encountered\n{result}")
                    #         else:
                    #             st.info(f"Upload completed\n{result}")

                    # Using st.progress to show progress
                    progress_indicator = st.progress(0.0)
                    remaining_seconds_placeholder = st.empty()
                    expected_end_time_placeholder = st.empty()
                    final_result = None

                    nodes = convert_legacy_node_records(data.get("nodes"), True, "_uid")
                    rels = convert_legacy_relationship_records(
                        data.get("relationships"), True, "_uid"
                    )
                    converted_data = {"nodes": nodes, "relationships": rels}

                    config = Neo4jConfig(
                        neo4j_uri=uri,
                        neo4j_user=user,
                        neo4j_password=password,
                        overwrite=should_overwrite,
                    )
                    for result in batch_upload_generator(
                        config=config,
                        data=converted_data,
                    ):
                        if result is None:
                            print(f"Unexpected result: {result}")
                            continue
                        completion = result.float_completed()
                        projected_sec = result.projected_seconds_to_complete()
                        progress_text = f"Upload {round(completion * 100)}% complete"

                        # Update progress indicatior + supporting text
                        progress_indicator.progress(completion, progress_text)
                        remaining_seconds_placeholder.text(
                            f"Remaining: {projected_sec} seconds"
                        )
                        expected_end_time_placeholder.text(
                            f"Expected completion:{result.projected_completion_time()}"
                        )
                        final_result = result

                    if final_result.was_successful == False:
                        st.error(f"Upload Errors encountered\n{result}")
                    else:
                        st.info(f"Upload completed\n{result}")
