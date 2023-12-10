import streamlit as st
import os
import logging
from PIL import Image

directory = 'graph_data_generator_streamlit/images/'

def samples_list():
    filenames = os.listdir(directory)
    filenames.sort()
    for filename in filenames:
        try:
            image = Image.open(os.path.join(directory, filename))
            st.image(image, caption=f'{filename}')
        except Exception as e:
            logging.error(e)
