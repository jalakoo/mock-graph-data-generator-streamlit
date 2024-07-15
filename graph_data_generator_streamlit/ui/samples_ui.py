import streamlit as st
import os
import logging
from PIL import Image

directory = "graph_data_generator_streamlit/images/"

# Limit verbose output from PIL library
logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL)
logging.getLogger("PIL.Image").setLevel(logging.CRITICAL)


def samples_list():
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

    if len(st.session_state["SAMPLE_IMAGES"]) == 0:
        filenames = os.listdir(directory)
        filenames.sort()
        for filename in filenames:
            if filename.lower().endswith(image_extensions) == False:
                # Skip any non-image files
                continue
            try:
                image = Image.open(os.path.join(directory, filename))
                st.image(image, caption=f"{filename}")
                st.session_state["SAMPLE_IMAGES"].append((image, filename))
            except Exception as e:
                logging.error(e)
    else:
        for image_filename in st.session_state["SAMPLE_IMAGES"]:
            try:
                st.image(image_filename[0], caption=image_filename[1])
            except Exception as e:
                logging.warning("Failed to load image: " + image_filename[1])
                pass
