from iot_agriculture import Payload


class SensorData(Payload):
    def __init__(self,
                 client_id: str = None,
                 light: bool = None,
                 water: bool = None,
                 time: str = None,
                 last_water=None,
                 temperature=None,
                 humidity=None,
                 *args,
                 **kwargs):
        super(SensorData, self).__init__(*args, **kwargs)
        self.client_id = client_id
        self.light = light
        self.water = water
        self.time = time
        self.last_water = last_water
        self.temperature = temperature
        self.humidity = humidity

    def to_db(self):
        return f"INSERT INTO sensor_data (client_id,light,water,time,last_water,temperature,humidity) VALUES " \
               f"('{self.client_id}', {self.light}, {self.water}, '{self.time}', '{self.last_water}', " \
               f"{self.temperature}, {self.humidity});"
