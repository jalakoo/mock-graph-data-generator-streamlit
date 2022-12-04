from file_utils import save_csv

def export_csv_node(
    filename: str,
    node_values: list[dict],
    export_folder: str):

    # remove trailing slash from export path if present
    cleaned_export_folder = export_folder.rstrip("/") 
    csv_filepath = f"{cleaned_export_folder}/{filename}"

    save_csv(filepath=csv_filepath, data=node_values)