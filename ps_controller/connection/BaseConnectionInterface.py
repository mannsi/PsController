class BaseConnectionInterface:
    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def connected(self):
        raise NotImplementedError()

    def clear_buffer(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def set(self, sending_data):
        raise NotImplementedError()