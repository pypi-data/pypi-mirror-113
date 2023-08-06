import abc
from generic_service_bus_cqrs.enum_type import MessageStatus
from generic_service_bus_cqrs.domain import ICommand, IEvent, ICorrelationContext

class IServiceBus(abc.ABC):
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def busPublisher() -> 'IBusPublisher':
        pass

    @abc.abstractmethod
    def busSubscriber() -> 'IBusSubscriber':
        pass
    
    @abc.abstractmethod
    def connect(self):
        pass
    
    @abc.abstractmethod
    def close(self):
        pass

class ICommandHandler(abc.ABC):
    @abc.abstractmethod
    def handle(command: ICommand, context: ICorrelationContext): 
        pass
    
class IEventHandler(abc.ABC):
    @abc.abstractmethod
    def handle(event: IEvent, context: ICorrelationContext): 
        pass
    
class IBusPublisher(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def sendAsync(self, command: ICommand, context: ICorrelationContext) -> MessageStatus:
        pass

    @abc.abstractmethod
    def publishAsync(self, event: IEvent, context: ICorrelationContext) -> MessageStatus:
        pass
    
    @abc.abstractmethod
    def close(self):
        pass
    
class IBusSubscriber(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def subscribeCommand(self, namespace:str, handler: ICommandHandler) -> 'IBusSubscriber':
        pass

    @abc.abstractmethod
    def subscribeEvent(self, namespace:str, handler: IEventHandler) -> 'IBusSubscriber':
        pass
    
    @abc.abstractmethod
    def close(self):
        pass
