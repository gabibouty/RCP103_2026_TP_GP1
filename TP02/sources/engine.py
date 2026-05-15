from enum import Enum
from typing import List

from sources.client import Client
from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
from sources.scheduler import Scheduler
from sources.server import Server
from sources.trace import generateTraceOut, generateTraceCSV

# There is 4 message by time unit
CLIENT_AVG_TIME: int = 4

# The server can handle 1 message by time unit
SERVER_AVG_TIME: int = 2


# TODO: Temp Constants
CLIENT_ID = 0
SERVER_ID = 1
TRANSMISSION_DURATION = 1.0


class TraceType(Enum):
    EVENT_LIST = 1
    STDIO = 2
    CSV = 3


class Engine:
    def __init__(self, t_simulation_duration: float):
        self.__simulation_duration: float = t_simulation_duration
        self.__message_count: int = 0

        self.__scheduler: Scheduler = Scheduler()
        self.__server: Server = Server(SERVER_ID, SERVER_AVG_TIME)
        self.__client: Client = Client(CLIENT_ID, SERVER_ID, CLIENT_AVG_TIME)
        # TODO: add queue limit when necessary
        self.__queue: Queue = Queue()

        # TODO: generate gateway

    def get_all_messages_count(self) -> int:
        return self.__message_count

    def log(self, t_trace_type: TraceType):
        if t_trace_type == TraceType.STDIO:
            generateTraceOut(self.__scheduler.get_passed_events())
        elif t_trace_type == TraceType.CSV:
            generateTraceCSV(self.__scheduler.get_passed_events())
        else:
            return self.__scheduler.get_passed_events()

    def run(self):
        event_id: int = 0

        # MAIN LOOP
        while self.__scheduler.get_current_time() < self.__simulation_duration:
            # Add messages to send if needed
            while (
                not self.__scheduler.has_events()
                or self.__client.get_next_msg_time()
                <= self.__scheduler.get_current_time()
            ):
                msg = self.__client.pop_message()
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.SEND_MSG, msg)
                )
                self.__message_count += 1
                event_id += 1

            # Try to dequeue if needed
            if not self.__queue.is_empty() and self.__server.is_free(
                self.__scheduler.get_current_time()
            ):
                msg = self.__queue.get()
                msg.set_message_server_time(self.__scheduler.get_current_time())
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.MSG_DEPT, msg)
                )
                event_id += 1
                self.__server.start_work(self.__scheduler.get_current_time())

            # Update scheduler
            event = self.__scheduler.pop_event()
            if event.get_event_type() == EventType.SEND_MSG:
                msg = event.get_message()
                msg.set_message_arrival_time(
                    event.get_event_time() + TRANSMISSION_DURATION
                )
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.RECV_MSG, msg)
                )
                event_id += 1
            elif event.get_event_type() == EventType.RECV_MSG:
                self.__queue.put(event.get_message())

        Message.reset_ids()
