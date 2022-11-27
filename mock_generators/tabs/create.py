import streamlit as st
from constants import *
from widgets.arguments import argument_widget
from new_generator import createGenerator
from models.generator import Generator

def create_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/blueprint.gif")
    with col2:
        st.write("Add additional generators for creating mock data with. Currently doesnt not clear after saving a new generator. Please go to the Generator tab to check if the generator was properly added.")
    st.markdown("--------")

    # TODO: Put into a reseting st.form

    # Make radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    type = st.radio("Generator Type", ["String", "Bool", "Int", "Float","Datetime"])
    name = st.text_input("Generator Name")
    description = st.text_input("Generator Description")
    # code_template = generic_template()
    with open(st.session_state[CODE_TEMPLATE_FILE], "r") as file:
        code_template = file.read()
    code = st.text_area("Generator Code", placeholder = code_template, height = 200, value = code_template)

    # Arguments
    num_cols = st.number_input("Number of Arguments", 0)

    # Adjust saved args from prior run
    prior_args = st.session_state[NEW_ARGS]
    if len(prior_args) > num_cols:
        new_args = prior_args[:num_cols]
        st.session_state[NEW_ARGS] = new_args

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