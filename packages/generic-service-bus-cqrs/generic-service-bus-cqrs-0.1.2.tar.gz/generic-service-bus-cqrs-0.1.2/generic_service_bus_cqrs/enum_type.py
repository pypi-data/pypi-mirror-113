import enum
class MessageStatus(enum.Enum):
   SUCCESS = 0
   FAILURE = 1
   CHANNEL_NOT_CREATED = 2
   INVALID_OBJECT_VALIDATION = 3
   CONNECTION_CLOSED = 4