import re
import redis
import json
import sched, time
from generic_service_bus_cqrs.enum_type import MessageStatus
from generic_service_bus_cqrs.options import RedisBusOptions
from generic_service_bus_cqrs.domain import ICommand, IEvent, IMessage, ICorrelationContext
from generic_service_bus_cqrs.interfaces import IServiceBus, IBusPublisher, IBusSubscriber, ICommandHandler, IEventHandler

class RedisServiceBus(IServiceBus):

    def __init__(self, options: RedisBusOptions):
        self.busPub = None
        self.busSub = None
        self.options = options

    def busPublisher(self):
        self.busPub = RedisBusPublisher(self.options)
        return self.busPub

    def busSubscriber(self):
        self.busSub = RedisBusSubscriber(self.options)
        return self.busSub
    
    def connect(self):
        pass
    
    def close(self):
        self.busPublisher.close()
        self.busSubscriber.close()
        
class RedisBusPublisher(IBusPublisher):
    def __init__(self, options: RedisBusOptions):
        self.options = options
        self.isChannelOpen = False
        self.channel = None
        self.createChannel()
        pass

    def sendAsync(self, command: ICommand, context: ICorrelationContext):
        return self.publishMessage(command, context)

    def publishAsync(self, event: IEvent, context: ICorrelationContext):
        return self.publishMessage(event, context)

    def publishMessage(self, message: IMessage, context: ICorrelationContext):
        if self.isChannelOpen == False:
            return MessageStatus.CHANNEL_NOT_CREATED

        topic = self.options.namespace + "/" + self.getTopicPreffix(message)

        msgJson = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        ctxJson = json.dumps(context, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
        msg = json.dumps({"content": msgJson,"context": ctxJson})

        self.channel.publish(topic, msg)

        return MessageStatus.SUCCESS

    def getTopicPreffix(self, message: IMessage):
        className = type(message).__name__
        string_list = re.findall('[A-Z][^A-Z]*', className)
        string_list_lowercase = [each_string.lower()
                                 for each_string in string_list]
        messageName = ".".join(string_list_lowercase)
        return messageName

    def createChannel(self):
        self.channel = redis.Redis(
            host=self.options.hostname, port=self.options.port, db=0)
        self.isChannelOpen = True

    def close(self):
        self.channel.close()
        

class RedisBusSubscriber(IBusSubscriber):
    def __init__(self, options: RedisBusOptions):
        self.options = options
        self.channel = None
        self.messageHandlerMap = {}
        
        self.s = None
        self.createChannel()
        self.listening = False

    def subscribeCommand(self, namespace:str, handler: ICommandHandler):
        return self.subscribeMessage(namespace, handler)

    def subscribeEvent(self, namespace:str, handler: IEventHandler):
        return self.subscribeMessage(namespace, handler)

    def subscribeMessage(self, namespace: str, handler):
        topic = self.getTopic(namespace, handler);
        self.channel.psubscribe(topic)
        self.messageHandlerMap[topic] = { "namespace": namespace, "handler": handler}
        
        if self.listening == False:
            self.listening = True
            self.s = sched.scheduler(time.time, time.sleep)
            self.s.enter(1, 1, self.startMonitoringMessage, ())
            self.s.run()
            #self.startMonitoringMessage()
        return self

    def getTopic(self, namespace: str, handler):
        className = type(handler).__name__
        string_list = re.findall('[A-Z][^A-Z]*', className)
        string_list_lowercase = [each_string.lower() for each_string in string_list]
        messageName = ".".join(string_list_lowercase[0:-1])
        prefix =  "*" if namespace == "" else namespace.strip()
        topic = prefix + "/" + messageName
        return topic

    def createChannel(self):
        p = redis.Redis(
            host=self.options.hostname, port=self.options.port, db=0)
        self.channel = p.pubsub()
        self.listening = False

    def startMonitoringMessage(self): 
        message = self.channel.get_message()
        if message:
            self.handleMessage(message)
        self.s.enter(1, 1, self.startMonitoringMessage, ())
        #while True:
            #message = self.channel.get_message()
            #if message:
                # do something with the message
                #print(message)
            #time.sleep(5)  # be nice to the system :)
    
    def handleMessage(self, message): 
        data = message['data']
        if (isinstance(data, bytes)):
            topic = message.get("pattern").decode("utf-8") 
            event_dict = json.loads(data.decode('utf-8'))
            content = event_dict['content']
            context = event_dict['context']
            msgHandl = self.messageHandlerMap.get(topic);
            handler = msgHandl.get("handler")
            eventName = self.getMessageNameFromHandler(handler)
            eventClass = type(eventName, (), content)
            contextClass = type('ICorrelationContext', (), context)
            handler.handle(eventClass(), contextClass())
        
    def getMessageNameFromHandler(self, handler):
        handlerName = type(handler).__name__
        eventName = handlerName.replace('Handler', '')
        return eventName
        
    def close(self):
        self.channel.close()
        self.listening = False