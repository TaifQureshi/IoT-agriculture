from iot_agriculture import Payload


class Responce(Payload):
    def __init__(self, received_uuid=None, status=None, *args, **kwargs):
        super(Responce, self).__init__(*args, **kwargs)
        self.received_uuid = received_uuid
        self.status = True
