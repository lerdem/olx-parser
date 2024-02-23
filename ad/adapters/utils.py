import configparser
from pathlib import Path

BASE_DIR = (
    Path(__file__).resolve(strict=True).parent.parent.parent
)  # project root dir = olx-parser-rss


def get_config() -> configparser.ConfigParser:
    config_file = BASE_DIR.joinpath('environment.ini')
    config = configparser.ConfigParser()
    with open(config_file) as raw_config_file:
        config.read_file(raw_config_file)
    return config
