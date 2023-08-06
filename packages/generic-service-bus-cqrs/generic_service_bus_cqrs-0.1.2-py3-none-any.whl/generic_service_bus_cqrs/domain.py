import abc

class IMessage(abc.ABC):
    def __init__(self):
        pass
    
class ICommand(IMessage, abc.ABC):
    def __init__(self):
        pass
    
class IEvent(IMessage, abc.ABC):
    def __init__(self):
        pass
    
class ICorrelationContext:
    def __init__(self):
        self.id = None
        self.userId = None
        self.resourceId = None
        self.connectionId = None
        self.name = None
        self.origin = None
        self.resource = None
        self.culture = None
        self.createdAt = None
        self.retries = 0
        