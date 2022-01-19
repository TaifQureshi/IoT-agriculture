import os
import yaml
import logging

logger = logging.getLogger("config")


class Config(object):
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.config = {}

    def add_config(self, path_list: list):
        for path in path_list:
            full_path = os.path.join(self.base_dir, path)
            if os.path.exists(full_path):
                logger.info(f"Loading configuration {path}")
                try:
                    config = yaml.safe_load(open(full_path, 'r'))
                    self.config.update(config)
                except Exception as e:
                    logger.error(path)
                    logger.exception(e)
            else:
                logger.info(f"Config {path} dose not exits at {full_path}")

    def get(self, key):
        return self.config.get(key, None)
