from generic_service_bus_cqrs.options import RedisBusOptions
from generic_service_bus_cqrs.interfaces import IServiceBus
from generic_service_bus_cqrs.redis_service_bus import RedisServiceBus

class ServiceBusBuilder:

    def useAMQP(self):
        return RedisBusBuilder();

    def useMQTT(self):
        return RedisBusBuilder();

    def useRedis(self):
        return RedisBusBuilder();
    

class RedisBusBuilder:
    
    def __init__(self):
        self.options = RedisBusOptions()
    
    def withNamespace(self, namespace = ""):
        self.options.namespace = namespace
        return self;

    def withHost(self, host = "localhost"):
        self.options.hostname = host
        return self;

    def withPort(self, port = 6379):
        self.options.port = port
        return self;

    def withReconnectTime(self, reconnectTime = 5000):
        self.options.reconnectTime = reconnectTime
        return self;

    def build(self) -> IServiceBus:
        return RedisServiceBus(self.options);