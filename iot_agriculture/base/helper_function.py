import os
import logging
import yaml
import sys


def base_setting(base_path="config", setting='base_setting.yml') -> dict:
    with open(os.path.join(base_path, setting), 'r') as file:
        documents = yaml.full_load(file)

    return documents


def get_logger(file_name, stdout=False):
    root = logging.getLogger()
    root.handlers = []

    formatter = logging.Formatter('%(asctime)s - %(name)10s - %(levelname)7s - %(message)s')
    handlers = []
    if stdout:
        handlers.append(logging.StreamHandler(sys.stdout))

    handlers.append(logging.FileHandler(filename=f"{file_name}.log"))
    for handler in handlers:
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        root.addHandler(handler)

    root.setLevel(logging.INFO)
    root.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++")
    root.info(f"logging file location: {file_name}")
    root.info(f"process started with stdout: {stdout}")
