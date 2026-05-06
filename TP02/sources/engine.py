from typing import List
import numpy as np

from sources.events_and_messages import Message, Event, EventType
from sources.scheduler import Scheduler

# There is 2 message by time unit
AVG_TIME: int = 2
LAMBDA: float = 1.0 / AVG_TIME


# TODO: Temp Constants
CLIENT_ID = 0
SERVER_ID = 1
TRANSMISSION_DURATION = 1.0


class Engine:
    def __init__(self, t_simulation_duration: float):
        self.__scheduler: Scheduler
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
                Message(msg_id, Message(msg_id, CLIENT_ID, SERVER_ID))
            )
            self.__mock_client[-1].set_message_time(t_timestamp=timestamp)
            x = rng.exponential(scale=LAMBDA, size=1)
            timestamp += x[0]
            msg_id += 1

    def run(self):
        event_id: int = 0
        while len(self.__mock_client) != 0 and self.__scheduler.has_events():
            if (
                not self.__scheduler.has_events()
                or self.__scheduler.get_current_time()
                <= self.__mock_client[0].get_message_send_time()
            ):
                msg = self.__mock_client.pop(0)
                self.__scheduler.add_event(
                    t_event=Event(
                        event_id, msg.get_message_send_time(), EventType.SEND_MSG, msg
                    )
                )
                event_id += 1

            event = self.__scheduler.pop_event()
            if event.get_event_type() == EventType.SEND_MSG:
                msg = event.get_message()
                msg.set_message_arrival_time(
                    event.get_event_time() + TRANSMISSION_DURATION
                )
                self.__scheduler.add_event(
                    t_event=Event(
                        event_id,
                        msg.get_message_arrival_time(),
                        EventType.RECV_MSG,
                        msg,
                    )
                )
                event_id += 1
                # TODO: transmit msg to gateway

            # TODO: call gateway process (== dequeue if server free, in this case add event)
