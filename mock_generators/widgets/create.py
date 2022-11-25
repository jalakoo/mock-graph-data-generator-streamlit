import streamlit as st
from constants import *
from template_selector import generic_template
from widgets.arguments import argument_widget
from new_generator import createGenerator
from models.generator import Generator

def create_tab():

    st.write("This is where you can add additional generators for creating mock data with.")
    st.markdown("--------")

    # Make radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    type = st.radio("Generator Type", ["String", "Bool", "Int", "Float","Datetime"])
    name = st.text_input("Generator Name")
    description = st.text_input("Generator Description")
    code_template = generic_template()
    code = st.text_area("Generator Code", placeholder = code_template, height = 200, value = code_template)

    # Arguments
    num_cols = st.number_input("Number of Arguments", 0)

    if num_cols > 0:
        for i in range(num_cols):
            st.markdown("""---""")
            argument_widget(i)

    # logging.info(f'args: {args}')

    code_filepath = st.session_state[CODE_FILE]
    spec_filepath = st.session_state[SPEC_FILE]
    generators = st.session_state[GENERATORS]
    args = st.session_state[NEW_ARGS]

    if st.button("Create Generator"):
        st.write("Creating generator...")
        success = createGenerator(
            code_filepath=code_filepath,
            spec_filepath=spec_filepath,
            existing=generators, 
            type=type, 
            name=name, 
            description=description, 
            code=code,
            args=args)
        if success:
            st.success("Generator created successfully")

        else:
            st.error("Could not create generator")