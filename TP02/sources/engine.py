from enum import Enum
from typing import List

from sources.client import Client
from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
from sources.scheduler import Scheduler
from sources.server import Server
from sources.trace import generateTraceOut, generateTraceCSV
from sources.gateway import Gateway
from sources.constants import SERVER_AVG_TIME, TRANSMISSION_DURATION




class TraceType(Enum):
    EVENT_LIST = 1
    STDIO = 2
    CSV = 3


class Engine:
    def __init__(
        self,
        t_simulation_duration: float,
        t_server_count: int,
        t_client_count: int,
        t_queue_limit: int = 4096,
    ):
        Message.reset_ids()
        Client.reset_avg_time_selector()
        self.__simulation_duration: float = t_simulation_duration

        self.__scheduler: Scheduler = Scheduler()

        self.__clients: List[Client] = []
        for i in range(t_client_count):
            self.__clients.append(Client(i + 1))

        self.__gateway: Gateway = Gateway(t_server_count=t_server_count, t_server_starting_count=self.__clients[-1].get_client_id() + 1, t_queue_limit=t_queue_limit)

    def log(self, t_trace_type: TraceType):
        if t_trace_type == TraceType.STDIO:
            generateTraceOut(self.__scheduler.get_passed_events())
        elif t_trace_type == TraceType.CSV:
            generateTraceCSV(self.__scheduler.get_passed_events())
        else:
            return self.__scheduler.get_passed_events()

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

                msg.set_message_arrival_time(
                    msg.get_message_send_time() + TRANSMISSION_DURATION
                )
                self.__scheduler.add_event(
                    t_event=Event(t_event_id, EventType.RECV_MSG, msg)
                )
                t_event_id += 1
        return t_event_id

    def __add_event(self,  msg_list: list[Message], t_event_id: int) -> int:
        if len(msg_list) != 0:
            for msg in msg_list:
                self.__scheduler.add_event(
                    t_event=Event(t_event_id, EventType.MSG_DEPT, msg)
                )
                t_event_id += 1
        return t_event_id

    def run(self):
        event_id: int = 0
        # MAIN LOOP
        event_id = self.__pop_messages_from_clients(event_id)
        while self.__scheduler.get_current_time() < self.__simulation_duration:
            time = self.__scheduler.get_current_time()

            event = self.__scheduler.pop_event()
            if event.get_event_type() == EventType.RECV_MSG:
                self.__gateway.send_message(event.get_message())

            msg_list = self.__gateway.try_start_server_job(time)
            event_id = self.__add_event(msg_list, event_id)

            event_id = self.__pop_messages_from_clients(event_id)

        Message.reset_ids()
        Client.reset_avg_time_selector()
