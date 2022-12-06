import streamlit as st
import os
import sys
import logging
from constants import *

def folder_files_expander(
    folder_path: str,
    specific_extension: str = None,
    show_hidden: bool = False,
    widget_id: str = ""):

    try:
        for path in os.scandir(folder_path):
            if path.is_file():
                if specific_extension != None:
                    if path.name.endswith(specific_extension) == False:
                        # logging.info(f'folder_files_expander: skipping file without extension {specific_extension}: {path.name}')
                        continue
                if show_hidden == False:
                    if path.name[0] == '.':
                        # logging.info(f'folder_files_expander: skipping hidden file: {path.name}')
                        continue
                # TODO: Update to check for other compression types?
                if path.name.endswith('.zip'):
                    with st.expander(path.name):
                        # try:
                        #     st.write(f'{path.stat().st_size} bytes')
                        # except OSError as e:
                        #     st.write(f'Error: reading zip file: {e}')

                        # TODO: verify this is our generated file
                        st.write(f"(Upload this file to Neo4j's data-importer)")
                        # Duplicative of the export tab - but a really convenient here.
                        try:
                            with open(f"{st.session_state[ZIPS_PATH]}/{DEFAULT_DATA_IMPORTER_FILENAME}.zip", "rb") as file:
                                st.download_button(label="Download", data=file, file_name=f"{DEFAULT_DATA_IMPORTER_FILENAME}.zip", mime="application/zip", key=f"generate_{path.name}_{widget_id}_download_button")
                        except:
                            st.warning("No data-importer zip found. Please generate data first.")
                            logging.error(f'Problem reading zip file: {path.name}: error: {sys.exc_info()[0]}')
                else:
                    with st.expander(path.name):
                        with open(path, 'r') as f:
                            st.text(f.read())

        # Alt method using os.walk
        # for root, dirs, files in os.walk(str(folder_path)):
        #     for file in files:
        #         if specific_extension:
        #             if not file.endswith(specific_extension):
        #                 continue
        #         if show_hidden == False:
        #             if file[0] == ".":
        #                 # Skip hidden files
        #                 continue
        #         # logging.info(f'Found file: {file}')
        #         with st.expander(file):
        #             with open(os.path.join(root, file), 'r') as f:
        #                 st.text(f.read())

    except:
        logging.error(f'Error reading files from folder {folder_path}: {sys.exc_info()[0]}')
        st.error(f'Could not retrieve files from export folder path: {folder_path}')