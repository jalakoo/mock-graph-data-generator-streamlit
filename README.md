# MOCK GRAPH DATA GENERATOR
This is a prototype app for generating mock graph data for [Neo4j](https://neo4j.com/) database instances.

The app uses [Streamlit](https://streamlit.io/) to create and manage the UI interface.


## Recommendations
Connect with a Chromium browser. Known issues when using with Safari, especially with interfacing with arrows and the data-importer.


## Running
Locally
```
pipenv shell
pipenv sync
pipenv run streamlit run mock_generators/app.py
```