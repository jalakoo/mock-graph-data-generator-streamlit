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

def _csv_row_values(values: list[dict])->list[list[str]]:
    # Generate rows for relationship .csv
    logging.info(f'_csv_row_values: values: {values}')
    result = []
    for a_dict in values:
        for _, v in a_dict.items():
            # TODO: This is a hack, but it works for now
            if type(v) is datetime:
                result.append(v.isoformat())
            else:
                result.append(v)
    return result

def _csv_headers(relationship: dict)->list[str]:
    # Generate column headers for .csv
    result = []
    for k in relationship.keys():
        result.append(k)
    return result

def export_csv_relationship(
    filename: str,
    values: list[dict],
    export_folder: str):

    # Sample incoming values:
    # [
    #  {
    #    "_uid": "n1_abc",
    #    "since": "2020-01-01"
    #   }
    # ]

    # remove trailing slash from export path if present
    cleaned_export_folder = export_folder.rstrip("/") 
    csv_filepath = f"{cleaned_export_folder}/{filename}"

    rows = _csv_row_values(values)
    logging.info(f'export_csv_relationship: values: {values}')
    header = _csv_headers(values[0])
    save_csv(filepath=csv_filepath, header=header, data=rows)