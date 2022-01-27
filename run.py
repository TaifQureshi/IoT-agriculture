import sys
import importlib
from iot_agriculture import set_logger, base_setting
import os
from typing import Dict

if __name__ == "__main__":
    program = "runners."
    inputs = []
    stdout = False
    if "--stdout" in sys.argv:
        stdout = True
    for i in sys.argv[1].split("."):
        inputs.append(i)

    program += inputs[0]
    model = importlib.import_module(program, package=None)
    config_location = os.getcwd() + '/config'
    config = base_setting(config_location, "base.yml")
    set_logger(f"{os.getcwd()}/{config.get('logger_path')}/{inputs[0]}", stdout=stdout)
    runner = getattr(model, inputs[0])
    pidfile_args: Dict[str, str] = {
        "pidname": inputs[0],
        "piddir": "/tmp",
        "register_term_signal_handler": "",
    }
    from pid import PidFile
    with PidFile(**pidfile_args):
        runner(inputs, config_location)
