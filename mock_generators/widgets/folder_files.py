import streamlit as st
import os
import sys
import logging
from constants import *

def folder_files_expander(
    folder_path: str,
    widget_id: str = "",
    # TODO: Update this to take a list
    specific_extension: str = None,
    show_hidden: bool = False,
    enable_delete_button: bool = False,
    enable_download: bool = False,
    download_button_text: str = "Download",
    file_selected: callable = None,
    file_selection_button_text: str = "Select",
    ):

    # TODO: Sorting

    try:
        paths = []
        for _path in os.scandir(folder_path):
            paths.append(_path)
        
        paths.sort(key=lambda x: x.name, reverse=True)
        for path in paths:
            if path.is_file():
                if specific_extension != None:
                    if path.name.endswith(specific_extension) == False:
                        continue
                if show_hidden == False:
                    if path.name[0] == '.':
                        continue

                # Display filename
                with st.expander(path.name):

                    # Can't nest columns in expanders already in columns, so have to display buttons top-to-bottom

                    if enable_download:
                        try:
                            # TODO: Finish making generic download feature
                            with open(path, "rb") as file:
                                st.download_button(label=download_button_text, data=file, file_name=f"{path.name}", mime="application/zip", key=f"generate_{path.name}_{widget_id}_download_button")
                        except:
                            st.warning("Problem downloading file.")
                            logging.error(f'Problem reading zip file: {path.name}: error: {sys.exc_info()[0]}')

                    if file_selected != None:
                        if st.button(file_selection_button_text, key=f"select_{path.name}_{widget_id}"):
                            file_selected(path)

                    # TODO: Delete button - does not work as expected below
                    # if enable_delete_button:
                    #     if st.button("Delete", key=f"delete_{path.name}_{widget_id}"):
                    #         os.remove(path)
                    #         st.experimental_rerun()

                    # TODO: Update to check for other compression types?

                    # Display file contents
                    if path.name.endswith('.zip') == False:
                        with open(path, 'r') as f:
                            st.text(f.read())

    except:
        logging.error(f'Error reading files from folder {folder_path}: {sys.exc_info()[0]}')
        st.error(f'Could not retrieve files from export folder path: {folder_path}. Does the folder exist?')