from models.mapping import Mapping
from models.node_mapping import NodeMapping
from models.property_mapping import PropertyMapping
from models.generator import Generator
import logging
from file_utils import save_csv
import sys
import logging

def export_csv_relationship(
    filename: str,
    values: list[dict],
    export_folder: str):

    # Sample incoming values:
    # [
    #  {
    #    "<from_node_key_property_name>": "n1_abc",
    #    "<to_node_key_property_name>": "n2_abc",
    #    "since": "2020-01-01"
    #   }
    # ]

    # remove trailing slash from export path if present
    cleaned_export_folder = export_folder.rstrip("/") 
    csv_filepath = f"{cleaned_export_folder}/{filename}"

    save_csv(filepath=csv_filepath, data=values)