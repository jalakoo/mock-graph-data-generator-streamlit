from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
from models.data_import import DataImporterJson
import logging
import datetime

def csv_rows_for_node_values(values: list[dict])->list[list[str]]:
    # Generate rows for node .csv
    result = []
    for value in values:
        for v in value.values():
            # TODO: This is a hack, but it works for now
            if type(v) is datetime:
                result.append(v.isoformat())
            else:
                result.append(v)
    return result

def csv_headers_for_nodes(a_node_value: dict)->list[str]:
    # Generate column headers for node .csv
    result = []
    for k in a_node_value.keys():
        result.append(k)
    return result

def export_csv_node(
    filename: str,
    node_values: list[dict],
    export_folder: str):

    # remove trailing slash from export path if present
    cleaned_export_folder = export_folder.rstrip("/") 
    csv_filepath = f"{cleaned_export_folder}/{filename}"

    rows = csv_rows_for_node_values(node_values)
    header = csv_headers_for_nodes(node_values[0])
    save_csv(filepath=csv_filepath, header=header, data=rows)