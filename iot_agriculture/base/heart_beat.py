from iot_agriculture import Payload


class HeartBeat(Payload):
    def __init__(self, client_id, count, *args, **kwargs):
        super(HeartBeat, self).__init__(*args, **kwargs)
        self.client_id = client_id
        self.count = count
