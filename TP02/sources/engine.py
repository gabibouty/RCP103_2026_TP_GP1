from enum import Enum

from sources.client import Client
from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
from sources.scheduler import Scheduler
from sources.server import Server
from sources.trace import generateTraceOut, generateTraceCSV

# There is 4 message by time unit
AVG_TIME: int = 4
LAMBDA: float = 1.0 / AVG_TIME

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
        self.__scheduler: Scheduler = Scheduler()
        self.__server: Server = Server(SERVER_ID, SERVER_AVG_TIME)
        self.__client: Client = Client(
            CLIENT_ID, SERVER_ID, t_simulation_duration, LAMBDA
        )
        # TODO: add queue limit when necessary
        self.__queue: Queue = Queue()

        # TODO: generate client
        # TODO: generate gateway

    def has_finished(self) -> bool:
        return not self.__client.has_messages() and not self.__scheduler.has_events()

    def log(self, t_trace_type: TraceType):
        if t_trace_type == TraceType.STDIO:
            generateTraceOut(self.__scheduler.get_passed_events())
        elif t_trace_type == TraceType.CSV:
            generateTraceCSV(self.__scheduler.get_passed_events())
        else:
            return self.__scheduler.get_passed_events()

    def run(self):
        event_id: int = 0
        while not self.has_finished():
            if (not self.__scheduler.has_events()) or (
                self.__client.has_messages()
                and self.__client.get_next_msg_time()
                <= self.__scheduler.get_current_time()
            ):
                msg = self.__client.pop_message()
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.SEND_MSG, msg)
                )
                event_id += 1

            event = self.__scheduler.pop_event()
            time = event.get_event_time()

            if not self.__queue.is_empty() and self.__server.is_free(time):
                msg = self.__queue.get()
                msg.set_message_server_time(time)
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.MSG_DEPT, msg)
                )
                event_id += 1
                self.__server.start_work(time)

            if event.get_event_type() == EventType.SEND_MSG:
                msg = event.get_message()
                msg.set_message_arrival_time(time + TRANSMISSION_DURATION)
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.RECV_MSG, msg)
                )
                event_id += 1
            elif event.get_event_type() == EventType.RECV_MSG:
                if self.__server.is_free(time):
                    msg = event.get_message()
                    msg.set_message_server_time(time)
                    self.__scheduler.add_event(
                        t_event=Event(event_id, EventType.MSG_DEPT, msg)
                    )
                    event_id += 1
                    self.__server.start_work(time)
                else:
                    self.__queue.put(event.get_message())

            # TODO: call gateway process (== dequeue if server free, in this case add event)
