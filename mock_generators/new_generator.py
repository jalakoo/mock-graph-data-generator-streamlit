import uuid
from file_utils import save_file, save_json
import logging
import sys
from models.generator import Generator, GeneratorArg, GeneratorType, generators_dict_to_json

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
    # new_generator_dict = {
    #     "name": name,
    #     "description": description,
    #     "type": type,
    #     "code_url": filename,
    #     "image_url": "",
    #     "args": args,
    # }

    new_generator = Generator(
        id = id,
        type = GeneratorType.typeFromString(type),
        name = name,
        description = description,
        code_url = filename,
        args = GeneratorArg.list_from(args)
    )
    existing[id] = new_generator
    json = generators_dict_to_json(existing)

    try:
        save_json("mock_generators/generators.json", json)
        return True
    except:
        logging.error(f"Could not save generators.json: {sys.exc_info()[0]}")
        return False