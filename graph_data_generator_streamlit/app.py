import streamlit as st
from ui.instructions_ui import instructions_ui
from ui.generate_ui import generate_ui
from ui.design_ui import arrows_ui, generators_ui
from ui.ideate_ui import ideate_ui
from ui.export_ui import export_ui
from ui.samples_ui import samples_list
import logging


# Heavy import support
import sys
from pathlib import Path
from streamlit.config import on_config_parsed
from streamlit.web import cli

# noinspection PyUnresolvedReferences
def heavy_imports() -> None:
    """For an explanation, please refer to this thread -
    https://discuss.streamlit.io/t/any-ideas-on-your-app-is-having-trouble-loading-the-
    st-aggrid-aggrid-component/10176/19?u=vovavili"""
    from streamlit_agraph import agraph, Node, Edge, Config


def main()-> None:

    # Heavy import support
    on_config_parsed(heavy_imports)
    sys.argv.extend(
        [
            "run",
            str(Path(__file__).resolve().parent / "app.py"),
            "--server.port=8080",
            "--server.address=0.0.0.0",
        ]
    )
    # cli.main(prog_name="streamlit")


    # SETUP
    st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(f'App Started')

    # Uncomment to start graph_data_generator logging
    # start_logging()

    # LOAD optional env data
    try:
        neo4j_uri = st.secrets.get("NEO4J_URI", None)
        neo4j_user = st.secrets.get("NEO4J_USER", None)
        open_ai_key = st.secrets.get("OPENAI_API_KEY", None)
        neo4j_pass = st.secrets.get("NEO4J_PASSWORD", None)
    except:
        neo4j_uri = None
        neo4j_user = None
        neo4j_pass = None
        open_ai_key = None
        pass

    if "NEO4J_URI" not in st.session_state:
        st.session_state["NEO4J_URI"] = neo4j_uri
    if "NEO4J_USER" not in st.session_state:
        st.session_state["NEO4J_USER"] = neo4j_user
    if "NEO4J_PASSWORD" not in st.session_state:
        st.session_state["NEO4J_PASSWORD"] = neo4j_pass
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state["OPENAI_API_KEY"] = open_ai_key

    # Setup other state info
    if "SAMPLE_PROMPT" not in st.session_state:
        st.session_state["SAMPLE_PROMPT"] = None
    if "DOWNLOADING" not in st.session_state:
        st.session_state["DOWNLOADING"] = False
    if "UPLOADING" not in st.session_state:
        st.session_state["UPLOADING"] = False
    if "ARROWS_DICT" not in st.session_state:
        st.session_state["ARROWS_DICT"] = None
    if "JSON_CONFIG" not in st.session_state:
        st.session_state["JSON_CONFIG"] = None
    if "SAMPLE_IMAGES" not in st.session_state:
        st.session_state["SAMPLE_IMAGES"] = []


    # Header
    instructions_ui()

    # Modify CSS to keep buttons closer together
    # st.markdown("""
    #             <style>
    #                 div[data-testid="column"] {
    #                     width: fit-content !important;
    #                     flex: unset;
    #                 }
    #                 div[data-testid="column"] * {
    #                     width: fit-content !important;
    #                 }
    #             </style>
    #             """, unsafe_allow_html=True)

    # Body
    st.markdown("**① DESIGN**")
    # design_ui()
    with st.expander("GraphGPT"):
        ideate_ui()
    with st.expander("Arrows"):
        arrows_ui()

    st.markdown("**② GENERATE**")
    generate_ui()

    export_ui()

    # Side bar
    with st.sidebar:
        tab1, tab2 = st.tabs(["Generators", "Samples"])
        with tab1:
            generators_ui()
        with tab2:
            samples_list()

if __name__ == "__main__":
    main()