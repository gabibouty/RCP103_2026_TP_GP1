from enum import Enum


class Message:
    def __init__(self, t_id: int, t_source: int, t_destination: int):
        self.__id: int = t_id
        self.__source: int = t_source
        self.__destination: int = t_destination
        self.__send_time: float = 0
        self.__arrival_time: float = 0
        self.__server_start: float = 0

    def get_message_id(self) -> int:
        return self.__id

    def get_message_time(self) -> float:
        return self.__timestamp

    def get_message_source(self) -> int:
        return self.__source

    def get_message_destination(self) -> int:
        return self.__destination

    def set_message_id(self, t_id: int):
        self.__id = t_id

    def set_message_time(self, t_timestamp: float) -> float:
        self.__timestamp = t_timestamp

    def set_message_source(self, t_source: int) -> int:
        self.__source = t_source

    def set_message_destination(self, t_destination: int) -> int:
        self.__destination = t_destination

    def __str__(self) -> str:
        return (
            f"Message:: Id: {self.__id} | "
            f"Source: {self.__source} | "
            f"Dest: {self.__destination} | "
            f"Timestamp: {self.__timestamp}"
        )


class EventType(Enum):
    SEND_MSG = 1
    RECV_MSG = 2
    MSG_DEPT = 3


class Event:
    def __init__(
        self, t_id: int, t_type: EventType, t_timestamp: float, t_message: Message
    ):
        self.__id: int = t_id
        self.__type: EventType = t_type
        self.__timestamp: float = t_timestamp
        self.__message: Message = t_message

    def get_event_time(self) -> float:
        return self.__timestamp

    def get_event_type(self) -> EventType:
        return self.__type

    def get_message(self) -> Message:
        return self.__message

    def set_event_time(self, t_timestamp: float):
        self.__timestamp = t_timestamp

    def set_event_type(self, t_type: EventType):
        self.__type = t_type

    def __str__(self) -> str:
        return (
            f"Event:: Id: {self.__id} | "
            f"Type: {self.__type} | "
            f"Timestamp: {self.__timestamp} | "
            f"Msg: {self.__message}"
        )
