# MOCK GRAPH DATA GENERATOR
This is a prototype app for generating mock graph data for [Neo4j](https://neo4j.com/) database instances.

<!-- TODO: Add animated gif: 1. Design in Arrows, 2. Mapping options, 3. Uploading to data-importer -->

## Requirements
[Poetry](https://python-poetry.org/) should be installed. Code in this repo uses Poetry for managing dependencies and running a virtual environment.

The app uses [Streamlit](https://streamlit.io/) to create and manage the UI interface.

## Running
Locally
`poetry run streamlit run mock_generators/app.py`