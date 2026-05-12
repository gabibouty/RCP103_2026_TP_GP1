from typing import List
import numpy as np

from sources.events_and_messages import Message, Event, EventType
from sources.scheduler import Scheduler
from sources.server import Server

# There is 4 message by time unit
AVG_TIME: int = 4
LAMBDA: float = 1.0 / AVG_TIME

# The server can handle 1 message by time unit
SERVER_AVG_TIME: int = 2


# TODO: Temp Constants
CLIENT_ID = 0
SERVER_ID = 1
TRANSMISSION_DURATION = 1.0


class Engine:
    def __init__(self, t_simulation_duration: float):
        self.__scheduler: Scheduler = Scheduler()
        self.__server: Server = Server(SERVER_ID, SERVER_AVG_TIME)
        self.__mock_client: List[Message] = []

        # TODO: generate client
        # TODO: generate gateway
        # TODO: generate server
        # TODO: generate scheduler

        # TODO: the following lines should be in client (don't forget to use unique id)
        timestamp = 0.0
        rng = np.random.default_rng(seed=1)
        msg_id: int = 0
        while timestamp < t_simulation_duration:
            self.__mock_client.append(
                Message(t_id=msg_id, t_source=CLIENT_ID, t_destination=SERVER_ID)
            )
            self.__mock_client[-1].set_message_send_time(t_timestamp=timestamp)
            x = rng.exponential(scale=LAMBDA, size=1)
            timestamp += x[0]
            msg_id += 1

    def has_finished(self) -> bool:
        return len(self.__mock_client) == 0 and not self.__scheduler.has_events()

    def run(self):
        event_id: int = 0
        while not self.has_finished():
            if not self.__scheduler.has_events() or (
                len(self.__mock_client) != 0
                and self.__scheduler.get_current_time()
                >= self.__mock_client[0].get_message_send_time()
            ):
                msg = self.__mock_client.pop(0)
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.SEND_MSG, msg)
                )
                event_id += 1

            event = self.__scheduler.pop_event()
            time = event.get_event_time()
            # trace
            if event.get_event_type() == EventType.SEND_MSG:
                msg = event.get_message()
                msg.set_message_arrival_time(time + TRANSMISSION_DURATION)
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.RECV_MSG, msg)
                )
                event_id += 1
                # TODO: transmit msg to gateway

            # TODO: for now, we don't have queue so if the server is free,
            # we can handle the message, else we drop it
            elif event.get_event_type() == EventType.RECV_MSG and self.__server.is_free(
                time
            ):
                msg = event.get_message()
                msg.set_message_server_time(time)
                self.__scheduler.add_event(
                    t_event=Event(event_id, EventType.MSG_DEPT, msg)
                )
                self.__server.start_work(time)

            # TODO: call gateway process (== dequeue if server free, in this case add event)
