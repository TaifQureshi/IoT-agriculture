from iot_agriculture import Payload
from uuid import uuid4


class SensorData(Payload):
    def __init__(self,
                 client_id: str,
                 light: bool,
                 water: bool,
                 time: str,
                 uuid=None,
                 *args,
                 **kwargs):
        super(SensorData, self).__init__(*args, **kwargs)
        self.client_id = client_id
        if uuid is None:
            self.uuid = uuid4()
        else:
            self.uuid = uuid
        self.light = light
        self.water = water
        self.time = time
