# MOCK GRAPH DATA GENERATOR
Applet using [Streamlit](https://streamlit.io) to conveniently design and generate interwoven mock data.

## Install Poetry
This applet uses [Poetry](https://python-poetry.org) for dependency management.

## Dependencies
This applet uses several packages that will auto-install if you use either the poetry or pipenv commands below. Notable is the use of 2 small packages:
1. [graph-data-generator](https://pypi.org/project/graph-data-generator/) for generating the actual mock data from a .json configuration
2. [neo4j-uploader](https://pypi.org/project/neo4j-uploader/) for uploading generated .json output to a [Neo4j](https://neo4j.com/developer/) graph database instance

## Running
```
poetry update
poetry run streamlit run graph_data_generator_streamlit/app.py
```

or 

```
pipenv shell
pipenv sync
pipenv run streamlit run graph_data_generator_streamlit/app.py 
```

## Testing with local packages
`poetry add --editable /path/to/package`
