from enum import Enum
from typing import List

from sources.client import Client
from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
from sources.scheduler import Scheduler
from sources.server import Server
from sources.trace import generateTraceOut, generateTraceCSV

# The server can handle 1 message by time unit
SERVER_AVG_TIME: int = 2

TRANSMISSION_DURATION = 1.0


class TraceType(Enum):
    EVENT_LIST = 1
    STDIO = 2
    CSV = 3


class Engine:
    def __init__(
        self,
        t_simulation_duration: float,
        t_flush_at_end: bool,
        t_server_count: int,
        t_client_count: int,
        t_queue_limit: int = 4096,
    ):
        Message.reset_ids()
        self.__simulation_duration: float = t_simulation_duration
        self.__flush_at_end: bool = t_flush_at_end

        self.__scheduler: Scheduler = Scheduler()

        self.__clients: List[Client] = []
        for i in range(t_client_count):
            self.__clients.append(Client(i + 1))

        self.__servers: List[Server] = []
        for i in range(t_server_count):
            self.__servers.append(Server(t_client_count + i + 1, SERVER_AVG_TIME))

        self.__queue: Queue = Queue(size=t_queue_limit)

        # TODO: generate gateway

    def log(self, t_trace_type: TraceType):
        if t_trace_type == TraceType.STDIO:
            generateTraceOut(self.__scheduler.get_passed_events())
        elif t_trace_type == TraceType.CSV:
            generateTraceCSV(self.__scheduler.get_passed_events())
        else:
            return self.__scheduler.get_passed_events()

    def __get_free_server(self, t_timestamp: float) -> Server:
        for server in self.__servers:
            if server.is_free(t_timestamp):
                return server
        return None

    def __get_next_workend(self) -> float:
        work_end = self.__servers[0].get_work_end()
        for server in self.__servers:
            work_end = min(work_end, server.get_work_end())
        return work_end

    def __get_next_messages_sending_time(self) -> float:
        next_sending_time = self.__clients[0].get_next_msg_time()
        for client in self.__clients:
            next_sending_time = min(next_sending_time, client.get_next_msg_time())
        return next_sending_time

    def __pop_messages_from_clients(self, t_event_id: int) -> int:
        time = (
            self.__scheduler.get_current_time()
            if self.__scheduler.has_events()
            else self.__get_next_messages_sending_time()
        )
        for client in self.__clients:
            while client.get_next_msg_time() <= time:
                msg = client.pop_message()
                self.__scheduler.add_event(
                    t_event=Event(t_event_id, EventType.SEND_MSG, msg)
                )
                t_event_id += 1
        return t_event_id

    def run(self):
        event_id: int = 0
        # MAIN LOOP
        while self.__scheduler.get_current_time() < self.__simulation_duration:
            # Add messages to send if needed
            event_id = self.__pop_messages_from_clients(event_id)

            # Try to dequeue if needed
            # TODO: for now we just study if the first server is free
            # but we have to check if one of them is free
            if not self.__queue.is_empty() and self.__servers[0].is_free(
                self.__scheduler.get_current_time()
            ):
                server = self.__get_free_server(self.__scheduler.get_current_time())
                if server != None:
                    msg = self.__queue.get()
                    msg.set_message_server_time(self.__scheduler.get_current_time())
                    msg.set_message_destination(server.get_id())
                    self.__scheduler.add_event(
                        t_event=Event(event_id, EventType.MSG_DEPT, msg)
                    )
                    event_id += 1
                    server.start_work(self.__scheduler.get_current_time())

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

        if self.__flush_at_end:
            while self.__scheduler.has_events() or not self.__queue.is_empty():
                time = (
                    self.__scheduler.get_current_time()
                    if self.__scheduler.has_events()
                    else self.__get_next_workend()
                )

                # Try to dequeue if needed
                if not self.__queue.is_empty() and self.__get_free_server(time) != None:
                    server = self.__get_free_server(time)
                    if server != None:
                        msg = self.__queue.get()
                        msg.set_message_server_time(time)
                        msg.set_message_destination(server.get_id())
                        self.__scheduler.add_event(
                            t_event=Event(event_id, EventType.MSG_DEPT, msg)
                        )
                        event_id += 1
                        server.start_work(time)

                # Update scheduler
                if self.__scheduler.has_events():
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
