class BaseSerializer:
    serializer: str

    def get_serializer_class(self):
        return self.serializer

    def serialize(self, obj):
        return obj

    def deserialize(self, data):
        return data
