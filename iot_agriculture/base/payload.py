import jsons


class Payload(object):
    def __init__(self, *args, **kwargs):
        ...

    @property
    def to_json(self):
        return jsons.dumps(self)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None

        return cls(**jsons.loads(data))
