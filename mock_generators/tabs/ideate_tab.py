import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import logging
from dotenv import load_dotenv
import os
import openai
import json

CHATGPT_KEY = "chatgpt"

def agraph_data_prompt(prompt: str)-> str:
    # Full prompt string to query openai with and finasse expected response
    full_prompt = f"""
    Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.

    If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2]. The relationship is directed, so the order matters.

    Each relationship must have 3 items in the list.
    Limit the number of relationships to 12.

    Example:
    prompt: Alice is Bob's roommate.
    updates:
    [["Alice", "roommate", "Bob"]]
    prompt: {prompt}
    updates:
    """
    return full_prompt

def agraph_data_from_reponse(response: str)->tuple[any, any, any]:
    # Returns agraph compatible nodes, edges, and config
    print(f'Response: {response}')
    # Response will be a list of 3 item tuples
    answers = json.loads(response)
    print(f'JSON: {answers}')
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
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=800,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
        )
    # TODO: Validate reponse
    print(f'OpenAI Response: {response}')
    return response.choices[0].text

def agraph_from_prompt(prompt: str):
    full_prompt = agraph_data_prompt(prompt)
    openai_response = generate_openai_response(full_prompt)
    nodes, edges, config = agraph_data_from_reponse(openai_response)
    if nodes is not None:
        agraph(nodes=nodes, 
            edges=edges, 
            config=config)
    
def ideate():
    with st.expander("Instructions"):
        st.markdown(
            """
        Not sure how to start with data modeling? Use this variation of GraphGPT to generate a graph data model from a prompt.
        1. Add your [OpenAI API Key](https://platform.openai.com/account/api-keys) to the OpenAI API Key field
        2. Enter in a prompt / narrative description of what you'd like modelled
        3. Download data as an arrows.app compatible JSON file
        4. Proceed to the '① Design' tab
        """
        )

    # Configure ChatGPT
    if CHATGPT_KEY not in st.session_state:
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        st.session_state[CHATGPT_KEY] = openai_api_key
    current_api = st.session_state[CHATGPT_KEY]
    new_api = st.text_input("OpenAI API Key", value=current_api, type="password")
    if new_api != current_api:
        st.session_state[CHATGPT_KEY] = new_api

    openai.api_key = st.session_state[CHATGPT_KEY]
    # logging.info(f'ideate_tab: ideate: ChatGPT API Key: {st.session_state[CHATGPT_KEY]}')

    # Display graph data from prompt
    prompt = st.text_input("Prompt")
    agraph_from_prompt(prompt)

    # Button to download graph data in arrows.app compatible JSON


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