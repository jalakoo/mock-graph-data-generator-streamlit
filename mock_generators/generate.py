import streamlit as st
from constants import *
from models.mapping import Mapping
from logic.generate_csv import generate_csv
from logic.generate_data_import import generate_data_importer_json
import os
import logging
import sys
import zipfile

def generate_zip(mapping: Mapping):
    import io 
    import csv
    import json
    import zipfile
    from models.data_import import DataImporterJson

    # Simple preprocess check
    if len(mapping.nodes) == 0:
        logging.error(f'No nodes to process from mapping: {mapping}')
    if len(mapping.relationships) == 0:
        logging.warning(f'No relationships found from mapping: {mapping}.')


    # Prep zip file to write data to
    in_memory_data = io.BytesIO()
    in_memory_zip = zipfile.ZipFile(
        in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
    in_memory_zip.debug = 3

    # Process nodes
    for nid, node in mapping.nodes.items():
        # Generate values from mappings
        values : list[dict] = node.generate_values()
        
        # Generate csv from values
        if values is None or values == []:
            logging.warning(f'No values generated for node {node.caption}')
            continue
    
        # Each node dataset will need it's own CSV file
        fieldnames = values[0].keys()
        nodes_buffer = io.StringIO()
        nodes_writer = csv.DictWriter(nodes_buffer, fieldnames=fieldnames)
        nodes_writer.writeheader()

        for row in values:
            try:
                nodes_writer.writerow(row)
            except Exception as e:
                logging.error(f'Problem writing row: {row}. Error: {e}')
        in_memory_zip.writestr(f"{node.filename()}.csv", nodes_buffer.getvalue())
    

    for rid, rel in mapping.relationships.items():
        # Generate values from mappings
        values : list[dict] = rel.generate_values()

        # Generate csv from values
        if values is None or values == []:
            logging.warning(f'No values generated for relationship {rel.type}')
            continue
        fieldnames = values[0].keys()
        rels_buffer = io.StringIO()
        writer = csv.DictWriter(rels_buffer, fieldnames=fieldnames)
        writer.writeheader()
        for row in values:
            writer.writerow(row)
        in_memory_zip.writestr(f"{rel.filename()}.csv", rels_buffer.getvalue())


    # generate data-importer.json
    dij = DataImporterJson()
    nodes = mapping.nodes
    dij.add_nodes(nodes)
    relationships = mapping.relationships
    dij.add_relationships(relationships)
    dij_dict = dij.to_dict()

    try:
        di_dump = json.dumps(dij_dict)
        in_memory_zip.writestr("neo4j_importer_model.json", di_dump)
        
    except Exception as e:
        logging.error(f'Error adding nodes and relationships for data-importer json: predump: {dij_dict}: \n\nError: {e}')

    return in_memory_data

# Local running or shared cloud data
def generate_data(mapping: Mapping):

    export_folder = st.session_state[EXPORTS_PATH]
    zips_folder = st.session_state[ZIPS_PATH]
    imported_filename = st.session_state[IMPORTED_FILENAME]

    # TODO: Implement better filename cleaning
    # TODO: Breaks when using a copy and pasted file
    export_zip_filename = f'{imported_filename}'.lower()
    export_zip_filename = export_zip_filename.replace(".json", "")
    export_zip_filename.replace(" ", "_")
    export_zip_filename.replace(".", "_")

    # Stop if no mapping data available
    if len(mapping.nodes) == 0:
        st.error('No nodes to generate data for. Map at least one noded.')
        st.stop()
        return

    # Generate values from mappings
    for _, node in mapping.nodes.items():
        # logging.info(f'Generating data for node: {node}')
        if len(node.properties) == 0:
            st.error(f'Node {node.caption} has no properties. Add at least one property to generate data.')
            st.stop()
            return
        node.generate_values()

    for _, rel in mapping.relationships.items():
        rel.generate_values()

    # Delete all files in export folder first
    dir = export_folder
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # Data Importer Options
    success = generate_csv(
        mapping, 
        export_folder=export_folder)

    # Check that data was generated
    if success == False:
        st.error('Error generating data. Check console for details.')
        # st.stop()
        # return

    success = generate_data_importer_json(
        mapping,
        export_folder=export_folder,
        export_filename=DEFAULT_DATA_IMPORTER_FILENAME)

    # Check that data-import data was generated
    if success == False:
        st.error('Error generating data-import json. Check console for details.')
        # st.stop()
        # return

    # Only attempt to zip files if data generation was successful
    if success:
        try:
            # Create zip file, appended with time created
            # now = str(datetime.now().isoformat())
            zip_path = f'{zips_folder}/{export_zip_filename}.zip'
            logging.info(f'generate_tab: Creating zip file: {zip_path}')
            with zipfile.ZipFile(f'{zip_path}', 'w', zipfile.ZIP_DEFLATED) as zipf:
                # zipdir(export_folder, zipf)
                path = export_folder
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file[0] =='.':
                            # Skip hidden files
                            continue
                        zipf.write(os.path.join(root, file), 
                                os.path.relpath(os.path.join(root, file), 
                                                os.path.join(path, '..')))
        except:
            st.error(f'Error creating zip file: {sys.exc_info()[0]}')
            # st.stop()
            return

    if success == True:
        st.success('Data generated successfully.')
