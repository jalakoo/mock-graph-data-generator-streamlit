import streamlit as st
from constants import *
from streamlit_extras.switch_page_button import switch_page

def header(
    title: str,
    description: str,
    color_name: str,
    prior_page: str = None,
    next_page: str = None,
):
    st.subheader(title)
    # st.write(
    #     f'<hr style="background-color: {color_name}; margin-top: 0;'
    #     ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
    #     unsafe_allow_html=True,
    # )
    if prior_page is None:
        h1, h2 = st.columns([5,1])
        with h1:
            st.caption(description)
        with h2:
            if next_page is not None:
                if st.button(f'{next_page} ➡️'):
                    switch_page(next_page.lower())
    else: 
        h1, h2, h3 = st.columns([1,4,1])
        with h1:
            if prior_page is not None:
                if st.button(f'⬅️ {prior_page}'):
                    switch_page(prior_page.lower())
        with h2:
            st.caption(description)
        with h3:
            if next_page is not None:
                if st.button(f'{next_page} ➡️'):
                    switch_page(next_page.lower())

    st.write(
        f'<hr style="background-color: {color_name}; margin-top: 0;'
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )