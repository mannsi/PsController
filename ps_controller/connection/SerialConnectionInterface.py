
class SerialConnectionInterface():
    def isOpen(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def read(self, number_of_bytes):
        raise NotImplementedError()

    def write(self, bytes):
        raise NotImplementedError()