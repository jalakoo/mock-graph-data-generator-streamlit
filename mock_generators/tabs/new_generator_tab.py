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
        st.write(f"Add additional generators.\n\nCreate new generators that can be used by properties in the mapping tab. These can be used to generate mock data for properties in the mapping tab.\n\nWhen finished, go to the Mapping Tab to assign generators to node/relationship properties or the Generators Tab to test and search for available generators.")
    st.markdown("--------")

    # TODO: Put into a resetting st.form

    # Make radio horizontal
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    with st.form("New Generator", clear_on_submit=True):
        # Generator type
        type = st.radio("Generator Type", ["String", "Bool", "Int", "Float","Datetime"],help="Generators are grouped by the data type they generate.")

        # Generator name
        name = st.text_input("Generator Name", help="The name of the generator. This will be used to reference the generator in the mapping tab. These should be unique but are not currently enforced.")
        description = st.text_input("Generator Description", help="A description of the generator. This will be displayed in the generator tab and the info roll-over in the mapping tab.")
        
        # Load example code
        with open(st.session_state[CODE_TEMPLATE_FILE], "r") as file:
            code_template = file.read()
        code = st.text_area("Generator Code", placeholder = code_template, height = 200, value = code_template, help="The code that will be executed to generate the mock data. This should be a function that takes a single argument, a dictionary of arguments, and returns a single value. The function name should not be changed from 'generate()'.")

        # Optional Arguments
        num_cols = st.number_input("Optional Number of Arguments", 0, help="Arguments that can be passed to the generator when it is called. For example, a generator that generates a random number between 0 and 1 can have optional arguments that specify lower and upper bounds of the random number.")

        args : list[dict] = []
        if num_cols > 0:
            for i in range(num_cols):
                st.markdown("""---""")
                args[i] = argument_widget(i)

        # logging.info(f'args: {args}')

        # Optional tags for auto-import completion
        tags_string = st.text_input("Optional Tags (comma separated)", help="Keyword tags for auto recommending generators to imported node and relationship properties.").lower()
        tags = tags_string.split(",")

        code_filepath = st.session_state[CODE_FILE]
        spec_filepath = st.session_state[SPEC_FILE]
        generators = st.session_state[GENERATORS]

        if st.form_submit_button("Save Generator"):
        # if st.button("Create Generator"):
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
                st.success("Generator created successfully")

            else:
                st.error("Could not create generator")