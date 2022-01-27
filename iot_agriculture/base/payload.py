import jsons


class Payload(object):
    _id_attrs = ()

    def __init__(self, *args, **kwargs):
        ...

    def __getitem__(self, item):
        return self.__dict__[item]

    def to_json(self):
        return jsons.dumps(self.to_dict())

    @classmethod
    def de_json(cls, data):
        if not data:
            return None

        return cls(**data)

    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value

        return data

    def __hash__(self):
        if self._id_attrs:
            return hash((self.__class__, self._id_attrs))  # pylint: disable=no-member
        return super(Payload, self).__hash__()
