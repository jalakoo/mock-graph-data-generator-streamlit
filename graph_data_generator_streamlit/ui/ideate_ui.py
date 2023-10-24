# Original ChatGPT ideation tab - needs updating to work

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import logging
import openai
import json

CHATGPT_KEY = "chatgpt"

def arrows_uri(json: dict) -> str:
    """
    Generates a URI for an arrows app visualization from a json object. WARNING! May overwrite existing arrows drawing.

    Args:
        json: A dictionary object representing an arrows compatible .json configuration

    Returns:
        A string URI for an arrows app visualization
    """
    # TODO: Convert the diction object into a base 64 json string
    json_string = json.dumps(json)
    base64_string = "unimplemented"
    result = f"https://arrows.app/#/import/json={base64_string}"
    return result

def agraph_data_prompt(prompt: str)-> str:
    # Full prompt string to query openai with and finasse expected response
    full_prompt = f"""
    Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.

    If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2]. The relationship is directed, so the order matters.

    Each relationship must have 3 items in the list.
    Limit the number of relationships to 12.
    Return only the data, do not explain.

    For example, the prompt: `Alice is Bob's roommate` should return [["Alice", "roommate", "Bob"]]

    prompt: {prompt}
    """
    return full_prompt


def convert_response(response: str | list) -> tuple[list, list]:
    """
    Converts an openai response into nodes and relationships

    Args:
        response: OpenAI response content
    
    Returns:
        A tuple of node labels and relationship types

    Raises:
        ...
    """
    raise NotImplementedError("Not implemented yet")

def agraph_data_from_reponse(response: str | list)->tuple[any, any, any]:
    # Returns agraph compatible nodes, edges, and config
    logging.debug(f'Response recieved: {response}')
    # Response will be a list of 3 item tuples
    if isinstance(response, str):
        answers = json.loads(response)
    elif isinstance(response, list):
        answers = response
    else:
        raise ValueError(f'Response is not a string or list. Response: {response}')

    logging.debug(f'JSON parsed: {answers}')
    nodes = []
    edges = []
    for idx, item in enumerate(answers):
        print(f'Item: {item}')
        n1 = item[0]
        r = item[1]
        n2 = item[2]
        n1id = f'{idx}_n1'
        n2id = f'{idx}_n2'
        node1 = Node(id=n1id, label=n1)
        node2 = Node(id=n2id, label=n2)
        edge = Edge(source=n1id, target=n2id, label=r)
        if node1 not in nodes:
            nodes.append(node1)
        if node2 not in nodes:
            nodes.append(node2)
        edges.append(edge)
    config = Config(width=800, height=800, directed=True)
    return (nodes, edges, config)

def generate_openai_response(prompt)-> str:
    # response = openai.chat.Completion.create(
    #     model="gpt-3.5-turbo",
    #     prompt=prompt,
    #     temperature=0.5,
    #     max_tokens=800,
    #     top_p=1.0,
    #     frequency_penalty=0.8,
    #     presence_penalty=0.0
    #     )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    # TODO: Validate reponse
    content = response.choices[0].message.content
    logging.debug(f'OpenAI Response: {response}, type: {type(content)}')
    return content

def agraph_from_prompt(prompt: str):
    full_prompt = agraph_data_prompt(prompt)
    openai_response = generate_openai_response(full_prompt)
    nodes, edges, config = agraph_data_from_reponse(openai_response)
    if nodes is not None:
        agraph(nodes=nodes, 
            edges=edges, 
            config=config)
    
def ideate_ui():
    # with st.expander("Instructions"):
    #     st.markdown(
    #     """
    #     Not sure how to start with data modeling? Use this variation of GraphGPT to generate a graph data model from a prompt.
    #     1. Add your [OpenAI API Key](https://platform.openai.com/account/api-keys) to the OpenAI API Key field
    #     2. Enter in a prompt / narrative description of what you'd like modelled
    #     3. Download data as an arrows.app compatible JSON file
    #     4. Proceed to the '① Design' tab
    #     """
    #     )

    # LOAD OPENAI KEY
    open_ai_key = st.secrets.get("OPENAI_API_KEY", None)
    if open_ai_key is None or open_ai_key == "":
        open_ai_key = st.session_state.get("OPENAI_API_KEY", None)
    else:
        st.session_state["OPENAI_API_KEY"] = open_ai_key

    # OPENAI TEXTFIELD
    new_open_ai_key = st.text_input(f'OpenAI KEY', type="password", value=open_ai_key)
    if new_open_ai_key != open_ai_key:
        st.session_state["OPENAI_API_KEY"] = new_open_ai_key

    openai.api_key = st.session_state.get("OPENAI_API_KEY", None)


    # Load a sample prompt
    sample_prompt = None
    if st.button("Sample prompt"):
        sample_prompt = "Sharks eat big fish. Big fish eat small fish. Small fish eat bugs."

    # Display Prompt
    prompt = st.text_input("Prompt", value=sample_prompt)
    if prompt is None or prompt == "":
        return
    agraph_from_prompt(prompt)

    # TODO: Button to download graph data in arrows.app compatible JSON
    if st.button("Copy .JSON", help="Output can be pasted into the ② GENERATE tab"):
        st.info("Not implemented yet")
    if st.button("Push to Arrows"):
        st.info("Not implemented yet")


def agraph_test():
    # Agraph
    nodes = []
    edges = []
    nodes.append( Node(id="Spiderman", 
                    label="Peter Parker", 
                    size=25, 
                    shape="circularImage",
                    image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") 
                ) # includes **kwargs
    nodes.append( Node(id="Captain_Marvel", 
                    size=25,
                    shape="circularImage",
                    image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png") 
                )
    edges.append( Edge(source="Captain_Marvel", 
                    label="friend_of", 
                    target="Spiderman", 
                    # **kwargs
                    ) 
                ) 

    config = Config(width=750,
                    height=950,
                    directed=True, 
                    physics=True, 
                    hierarchical=False,
                    # **kwargs
                    )

    agraph(nodes=nodes, 
            edges=edges, 
            config=config)