import streamlit as st
import os
import logging
from PIL import Image

directory = 'graph_data_generator_streamlit/images/'


def samples_list():
    if len(st.session_state["SAMPLE_IMAGES"]) == 0:
        filenames = os.listdir(directory)
        filenames.sort()
        for filename in filenames:
            try:
                image = Image.open(os.path.join(directory, filename))
                st.image(image, caption=f'{filename}')
                st.session_state["SAMPLE_IMAGES"].append((image, filename))
            except Exception as e:
                logging.error(e)
    else:
        for image_filename in st.session_state["SAMPLE_IMAGES"]:
            st.image(image_filename[0], caption=image_filename[1])
