class RedisBusOptions:
    
    def __init__(self):
        self.namespace = ""
        self.hostname = "localhost"
        self.port = 6379
        self.reconnectTime = 5000