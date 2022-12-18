import streamlit as st
from constants import *
from widgets.arguments import new_generator_argument
from new_generator import createGenerator
from models.generator import Generator

def create_tab():

    col1, col2 = st.columns([1,11])
    with col1:
        st.image("mock_generators/media/blueprint.gif")
    with col2:
        st.write(f"Add additional generators.\n\nCreate new generators that can be used by properties in the mapping tab.\n\nWhen finished, go to Generators Tab to test and search for available generators.")
    st.markdown("--------")

    # Make radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # st.form sadly does not support dynamic widget generation internally.
    # TODO: Either create a custom way to clear all inputs after submission or reduce need to dynamically change code template / optional arg fields
    # with st.form("New Generator", clear_on_submit=True):
    st.info(f'NOTE: Creating a new generator DOES NOT clear fields. Go to the Generators Tab to review new generators.')

    # Generator type
    type = st.radio("Generator Type", ["String", "Bool", "Int", "Float","Datetime", "Assignment"],help="Generators are grouped by the data type they generate.")

    ng1, ng2, ng3 = st.columns(3)

    with ng1:
        # Generator name
        name = st.text_input("Generator Name", help="Name the generator. This will be used to reference the generator in the Mapping Tab. These should be unique but are not currently enforced.")

    with ng2:
        # Generator description
        description = st.text_input("Generator Description", help="A description of the generator. This will be displayed in the generator tab and the info roll-over in the mapping tab.")
    
    with ng3:
        # Optional tags for auto-import completion
        tags_string = st.text_input("Optional Tags (comma separated)", help="Keyword tags for auto recommending generators to imported node and relationship properties.").lower()
        # TODO: Clear whitespaces between delimiters but not words
        tags = tags_string.split(",")

    # Load example code
    if type == "Relationship":
        with open("mock_generators/template_generators/relationship_generator.py", "r") as file:
            code_template = file.read()
            st.session_state["NEW_GENERATOR_CURRENT_TEMPLATE"] = code_template
    if type == "Assignment":
        with open("mock_generators/template_generators/assignment_generator.py", "r") as file:
            code_template = file.read()
            st.session_state["NEW_GENERATOR_CURRENT_TEMPLATE"] = code_template
    else:  
        # Use Generic
        with open(st.session_state[CODE_TEMPLATE_FILE], "r") as file:
            code_template = file.read()
            st.session_state["NEW_GENERATOR_CURRENT_TEMPLATE"] = code_template

    code = st.text_area("Generator Code", placeholder = st.session_state["NEW_GENERATOR_CURRENT_TEMPLATE"], height = 200, value = code_template, help="The code that will be executed to generate the mock data. This should be a function that takes a single argument, a dictionary of arguments, and returns a single value. The function name should not be changed from 'generate()'.")

    # Optional Arguments


    # The below method of dynamically adding UI elements does not work in an st.forms
    num_cols = st.number_input("Optional Number of Arguments", 0, help="Arguments that can be passed to the generator when it is called. For example, a generator that generates a random number between 0 and 1 can have optional arguments that specify lower and upper bounds of the random number.")
    args : list[dict] = []
    if num_cols > 0:
        for i in range(num_cols):
            st.markdown("""---""")
            new_arg = new_generator_argument(index=i, type=type)
            if new_arg:
                args.append(new_arg)

    # If using an st.form have to hardcode number of possible argument inputs
    # args : list[dict] = []
    # num_args = 4
    # cols = st.columns(num_args)
    # for c in range(num_args):
    #     with cols[c]:
    #         new_arg = new_generator_argument(index=c, type=type)
    #         if new_arg:
    #             args.append(new_arg)

    code_filepath = st.session_state[CODE_FILE]
    spec_filepath = st.session_state[SPEC_FILE]
    generators = st.session_state[GENERATORS]

    # if st.form_submit_button("Save Generator"):
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
            args=args,
            tags=tags)
        if success:
            st.success("Generator created successfully. Fields DO NOT currently clear after submission.")
        else:
            st.error("Could not create generator")