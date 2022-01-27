from iot_agriculture.server import DbConnection
from iot_agriculture import Config, set_logger, base_setting
import os

location = os.getcwd() + '\\config'
config = base_setting(location, "base.yml")
set_logger(f"{config.get('logger_path')}/test", stdout=True)
config = Config(location)
config.add_config(['server.yml'])

db = DbConnection(config.get("db"))
connect = db.connect()
if connect:
    print("connected")
    query = "Insert I"
else:
    print("not connected")
