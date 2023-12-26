import json
import logging
import os


log = logging.getLogger('discord')


def read_json_file(file_path: str) -> dict:
    log.debug(f'reading json from {file_path}')

    with open(file_path, 'r') as file:
        return json.load(file)


def write_json_file(json_: dict, file_path: str) -> None:
    log.debug(f'writing json to file {file_path}')

    with open(file_path, 'w') as file:
        json.dump(json_, file, indent=4)
