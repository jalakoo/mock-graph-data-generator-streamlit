import streamlit as st
import os
import sys
import logging
from constants import *

def folder_files_expander(
    folder_path: str,
    widget_id: str = "",
    specific_extension: str = None,
    show_hidden: bool = False,
    enable_download: bool = False,
    download_button_text: str = "Download",
    file_selected: callable = None,
    file_selection_button_text: str = "Select",
    ):

    try:
        for path in os.scandir(folder_path):
            if path.is_file():
                if specific_extension != None:
                    if path.name.endswith(specific_extension) == False:
                        continue
                if show_hidden == False:
                    if path.name[0] == '.':
                        continue

                # Display filename
                with st.expander(path.name):
                        if enable_download:
                            try:
                                # TODO: Finish making generic download feature
                                with open(path, "rb") as file:
                                    st.download_button(label=download_button_text, data=file, file_name=f"{path.name}", mime="application/zip", key=f"generate_{path.name}_{widget_id}_download_button")
                            except:
                                st.warning("Problem downloading file.")
                                logging.error(f'Problem reading zip file: {path.name}: error: {sys.exc_info()[0]}')
                            # try:
                            #     with open(f"{st.session_state[ZIPS_PATH]}/{DEFAULT_DATA_IMPORTER_FILENAME}.zip", "rb") as file:
                            #         st.download_button(label="Download", data=file, file_name=f"{DEFAULT_DATA_IMPORTER_FILENAME}.zip", mime="application/zip", key=f"generate_{path.name}_{widget_id}_download_button")
                            # except:
                            #     st.warning("No data-importer zip found. Please generate data first.")
                            #     logging.error(f'Problem reading zip file: {path.name}: error: {sys.exc_info()[0]}')

                        if file_selected != None:
                            if st.button(f"Select", key=f"select_{path.name}_{widget_id}"):
                                file_selected(path)

                        # TODO: Update to check for other compression types?

                        if path.name.endswith('.zip') == False:
                            with open(path, 'r') as f:
                                st.text(f.read())

    except:
        logging.error(f'Error reading files from folder {folder_path}: {sys.exc_info()[0]}')
        st.error(f'Could not retrieve files from export folder path: {folder_path}. Does the folder exist?')