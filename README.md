# MOCK GRAPH DATA GENERATOR

Applet using [Streamlit](https://streamlit.io) to conveniently design and generate interwoven mock data. A running cloud instance of this can be found [here](https://dev.neo4j.com/mock-graph-data-generator)

## Install Poetry

This applet uses [Poetry](https://python-poetry.org) for dependency management.

## Dependencies

This applet uses several packages that will auto-install if you use either the poetry or pipenv commands below. Notable is the use of 2 small packages:

1. [graph-data-generator](https://pypi.org/project/graph-data-generator/) for generating the actual mock data from a .json configuration
2. [neo4j-uploader](https://pypi.org/project/neo4j-uploader/) for uploading generated .json output to a [Neo4j](https://neo4j.com/developer/) graph database instance

## Local Running

```
poetry update
poetry run streamlit run graph_data_generator_streamlit/app.py
```

## Testing with local packages

`poetry add --editable /path/to/package`

## Running in Google Cloud

- Set up a [Google Cloud account](https://cloud.google.com)
- Create a [Google Cloud Project](https://developers.google.com/workspace/guides/create-project)
- [Enable billing](https://cloud.google.com/billing/docs/how-to/modify-project) for that project
- Temporarily move any .streamlit/secret.toml file to the root folder director (same level as Dockerfile)
- Install [glcoud cli](https://cloud.google.com/sdk/docs/install)
- Run the following commands from the terminal of your local dev machine:

```
gcloud builds submit --tag gcr.io/<google_cloud_project_id>/mock-graph-generator
gcloud run deploy --image gcr.io/<google_cloud_project_id>/mock-graph-generator --platform managed --allow-unauthenticated

When completed, can move secrets.toml file back to .streamlit/ - that or maintain a separate external secrets.toml file just for Google Cloud
```
