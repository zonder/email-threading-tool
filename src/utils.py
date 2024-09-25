import configparser
from typing import Any, Tuple

import yaml


def load_config(config_file: str) -> Tuple[str, str]:
    config = configparser.ConfigParser()
    config.read(config_file)
    client_secret = config.get('nylas', 'client_secret')
    return client_secret


def load_yaml(file_path: str) -> Any:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
