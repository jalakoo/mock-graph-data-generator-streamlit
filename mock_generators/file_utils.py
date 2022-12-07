import json
import os
import logging
import dataclasses, json
import csv
import io

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def load_string(filepath: str, default=None):
    if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
         with io.open(os.path.join(filepath), 'r') as _:
            logging.info(f"file_utils.py: No file at {filepath}")
            return default
    with open(filepath, 'r') as f:
        return f.read()

def load_json(filepath: str, default=None):
    """
    Create or load a file

    Loads an exiting file if it exists, otherwise creates a new one.

    Parameters:
    filepath (str): Filepath to the file to be created or loaded.

    Returns:
    A file object.

    """
    # file = load_file(filepath, default)
    # return json.load(file)
    if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
         with io.open(os.path.join(filepath), 'w') as db_file:
            logging.info(f"file_utils.py: Creating new file at {filepath}")
            db_file.write(json.dumps(default))
    with open(filepath, 'r') as f:
        return json.load(f)

def load_json_as_list(filepath: str, default=None) -> list[any]:
    file = load_json(filepath, default)
    return json.dumps(file)

def save_file(filepath, data):
    """
    Save a file
    
    Parameters:
    filepath (str): Filepath to the file to be saved.
    data (str): Data to be saved to the file.

    Returns:
    A file object.

    """
    if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
        with io.open(os.path.join(filepath), 'w') as db_file:
            logging.info(f"file_utils.py: Creating new file at {filepath}")
            db_file.write("")
    with open(filepath, 'w+') as f:
        f.write(data) 

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, cls=EnhancedJSONEncoder, indent=4, sort_keys=True)
        
# Using a different incoming data format.
# def save_csv(filepath: str, data=list[any], header=list[str]):
#     with open(filepath, 'w') as f:
#         writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
#         writer.writerow(header)
#         for row in data:
#             writer.writerow([row])

def save_csv(filepath: str, data: list[dict]):
    with open(filepath, 'w') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def export_data(output_path: str, filename: str, csv_headers: list[str], data: any):
    json_path = f'{output_path}{filename}.json'
    save_json(json_path, data)
    csv_path = f'{output_path}{filename}.csv'
    save_csv(csv_path, data, header=csv_headers)
    logging.info(f"file_utils.py: Exported data to paths: csv: {csv_path}")