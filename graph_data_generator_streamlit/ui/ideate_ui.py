# Original ChatGPT ideation tab - needs updating to work

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import logging
import openai
import json

# Yes yes - move all the non-ui stuff into a controller or something already

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


def agraph_from_response(response: str | list) -> tuple[list[Node], list[Edge]]:
    """
    Converts an openai response into agraph nodes and relationships

    Args:
        response: String or list in the format of [["node_id_string", "edge_id_string", "another_node_id_string"],...]
    
    Returns:
        A tuple of agraph nodes in a list and agraph edges in a list

    Raises:
        ...
    """
    logging.debug(f'Response recieved: {response}')
    # Response will be a list of 3 item tuples

    # Convert to list of lists - if needed
    if isinstance(response, str):
        answers = json.loads(response)
    elif isinstance(response, list):
        answers = response
    else:
        raise ValueError(f'Response is not a string or list. Response: {response}')

    logging.debug(f'JSON parsed: {answers}')
    nodes = set()
    result_edges = []
    for item in answers:
        # Each should be a tuple of 3 items, node-edge-node
        n1 = item[0]
        r = item[1]
        n2 = item[2]

        # Standardize casing
        r = r.upper()
        n1 = n1.title()
        n2 = n2.title()
        nodes.add(n1)
        nodes.add(n2) 

        edge = Edge(source=n1, target=n2, label=r)
        result_edges.append(edge)

    result_nodes = []
    for node_label in list(nodes):
        node = Node(id=node_label, label=node_label)
        result_nodes.append(node)

    logging.debug(f'Nodes returning: {result_nodes}')
    logging.debug(f'Edges returning: {result_edges}')

    return result_nodes, result_edges



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
    nodes, edges = agraph_from_response(openai_response)
    config = Config(width=800, height=800, directed=True)

    if nodes is not None:
        agraph(nodes=nodes, 
            edges=edges, 
            config=config)
    
def agraph_from_sample(prompt: str):
    # TODO: Pull from a file of samples
    openai_response = '[["Sharks", "eat", "big fish"], ["Big fish", "eat", "small fish"], ["Small fish", "eat", "bugs"]]'
    nodes, edges = agraph_from_response(openai_response)
    config = Config(height=400, width=1000, directed=True)

    if nodes is not None:
        agraph(nodes=nodes, 
            edges=edges, 
            config=config) 

def ideate_ui():

    st.markdown("Use a variation of Varun Shenoy's original [GraphGPT](https://graphgpt.vercel.app) to convert a natural language description into a graph data model")

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
    if st.button("Load Sample", key="graphgpt_load_sample"):
        sample_prompt = "Sharks eat big fish. Big fish eat small fish. Small fish eat bugs."

    # Display Prompt
    prompt = st.text_input("Prompt", value=sample_prompt)
    if prompt is None or prompt == "":
        return
    
    if prompt == sample_prompt:
        agraph_from_sample(prompt)
    else:
        agraph_from_prompt(prompt)

    # TODO: Button to download graph data in arrows.app compatible JSON
    g1, g2, g3 = st.columns([1,1,3])
    with g1:
        if st.button("Copy .JSON", help="Output can be pasted into the ② GENERATE tab"):
            st.info("Not implemented yet")
    with g2:
        if st.button("Edit in Arrows"):
            st.info("Not implemented yet")


# def agraph_sample():
#     # Agraph
#     nodes = []
#     edges = []
#     nodes.append( Node(id="Spiderman", 
#                     label="Peter Parker", 
#                     size=25, 
#                     shape="circularImage",
#                     image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") 
#                 ) # includes **kwargs
#     nodes.append( Node(id="Captain_Marvel", 
#                     size=25,
#                     shape="circularImage",
#                     image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png") 
#                 )
#     edges.append( Edge(source="Captain_Marvel", 
#                     label="friend_of", 
#                     target="Spiderman", 
#                     # **kwargs
#                     ) 
#                 ) 

#     config = Config(width=750,
#                     height=950,
#                     directed=True, 
#                     physics=True, 
#                     hierarchical=False,
#                     # **kwargs
#                     )

#     agraph(nodes=nodes, 
#             edges=edges, 
#             config=config)