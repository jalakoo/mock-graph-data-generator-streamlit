import uuid
from file_utils import save_file, save_json
import logging
import sys

def createGenerator(
    existing: dict,
    type: str,
    name: str,
    description: str,
    code: str,
    args: list[dict]
) -> bool:
    #  Generate new id
    id = str(uuid.uuid4())[:8]
    while id in existing.keys():
        id = str(uuid.uuid4())[:8]

    # Save code to file
    filename = f"mock_generators/generators/{id}.py"
    save_file(filename, code)

    # Save generator entry to generators.json
    new_generator_dict = {
        "name": name,
        "description": description,
        "type": type,
        "code_url": filename,
        "image_url": "",
        "args": args,
    }
    # existing.update({id: new_generator_dict})
    existing[id] = new_generator_dict
    try:
        save_json("mock_generators/generators.json", existing)
        return True
    except:
        logging.error(f"Could not save generators.json: {sys.exc_info()[0]}")
        return False