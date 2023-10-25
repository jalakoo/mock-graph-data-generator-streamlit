import streamlit as st

def config_ui():

    # LOAD OPENAI KEY
    # open_ai_key = st.secrets.get("OPENAI_API_KEY", None)
    # if open_ai_key is None or open_ai_key == "":
    #     open_ai_key = st.session_state.get("OPENAI_API_KEY", None)
    # else:
    #     st.session_state["OPENAI_API_KEY"] = open_ai_key

    # new_open_ai_key = st.text_input(f'OpenAI KEY', type="password", value=open_ai_key)
    # if new_open_ai_key != open_ai_key:
    #     st.session_state["OPENAI_API_KEY"] = new_open_ai_key

    # # LOAD NEO4J URI
    # neo4j_uri = st.secrets.get("NEO4J_URI", None)
    # if neo4j_uri is None or neo4j_uri == "":
    #     neo4j_uri = st.session_state.get("NEO4J_URI", None)
    # else:
    #     st.session_state["NEO4J_URI"] = neo4j_uri

    # new_neo4j_uri = st.text_input(f'Neo4j URI', value = neo4j_uri)
    # if new_neo4j_uri != neo4j_uri:
    #     st.session_state["NEO4J_URI"] = new_neo4j_uri

    # # NEO4J USER
    # neo4j_user = st.secrets.get("NEO4J_USER", None)
    # if neo4j_user is None or neo4j_user == "":
    #     neo4j_user = st.session_state.get("NEO4J_USER", None)
    # else:
    #     st.session_state["NEO4J_USER"] = neo4j_user
    

    # new_neo4j_user = st.text_input(f'Neo4j USER', value = neo4j_user, placeholder = "neo4j")
    # if new_neo4j_uri != neo4j_user:
    #     st.session_state["NEO4J_USER"] = new_neo4j_user

    # # NEO4J PASSWORD
    # neo4j_pass = st.secrets.get("NEO4J_PASSWORD", None)
    # if neo4j_pass is None or neo4j_pass == "":
    #     neo4j_pass = st.session_state.get("NEO4J_PASSWORD", None)
    # else:
    #     st.session_state["NEO4J_PASSWORD"] = neo4j_pass

    # new_neo4j_pass = st.text_input(f'Neo4j PASSWORD', type = "password", value = neo4j_pass)
    # if new_neo4j_pass != neo4j_pass:
    #     st.session_state["NEO4J_PASSWORD"] = new_neo4j_pass

    # Display current app version
    # TODO: Pull this directly from the pyproject.toml
    version = "0.7.1"
    st.write(f"Version {version}")