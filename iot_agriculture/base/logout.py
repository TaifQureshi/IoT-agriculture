from iot_agriculture import Payload


class Logout(Payload):
    def __init__(self, client_id, *args, **kwargs):
        super(Logout, self).__init__(*args, **kwargs)
        self.client_id = client_id
