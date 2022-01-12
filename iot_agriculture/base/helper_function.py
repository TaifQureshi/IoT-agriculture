import os
import logging
import yaml


def base_setting(setting='base_setting.yml') -> dict:
    with open(f'config/{setting}', 'r') as file:
        documents = yaml.full_load(file)

    return documents


def get_logger(path, name):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    os.makedirs(path, exist_ok=True)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] - %(message)s')
    logger = logging.getLogger(name)

    for handler in logger.root.handlers[:]:
        logger.root.removeHandler(handler)

    if not logger.hasHandlers():
        # Create handlers
        f_handler = logging.FileHandler(os.path.join(path, f"{name}.log"))
        c_handler = logging.StreamHandler()
        f_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        c_handler.setFormatter(c_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger


if __name__ == '__main__':
    data = base_setting()
    print(type(data['pricer'].get("port")))
