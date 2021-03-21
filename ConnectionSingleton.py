class ConnectionSingleton:

    __instance = None
    __address = None
    __port = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, address, port):
        if cls.__instance is None:
            print('New instance')
            cls.__instance = cls.__new__(cls)
            __address = address
            __port = port
            cls.__connect(__address, __port)
        else:
            raise RuntimeError('Dispose before creating another instance')
        return cls.__instance

    @classmethod
    def dispose(cls):
        cls.__instance = None
        print("Instance disposed")

    @staticmethod
    def __connect(address, port):
        print("Connected to " + address + " " + port)

    @classmethod
    def send(cls):
        print("Message Sent")

    @classmethod
    def receive(cls):
        print("Message Received")
