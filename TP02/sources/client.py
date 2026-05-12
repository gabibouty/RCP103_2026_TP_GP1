import numpy as np

from typing import List
from sources.events_and_messages import Message

# TODO:
#   - Id, List(Message)
#
#   - @Init ==> create message list
#   - get_next_msg_time ()
#   - pop_message ()
#


class Client:
    def __init__(
        self,
        t_id: int,
        t_destination: int,
        t_simulation_duration: float,
        t_lambda: float,
    ):
        self.__id = t_id
        self.__messages: List[Message] = []
        timestamp = 0.0
        rng = np.random.default_rng(seed=t_id)
        msg_id: int = 0
        while timestamp < t_simulation_duration:
            self.__messages.append(
                Message(t_id=msg_id, t_source=t_id, t_destination=t_destination)
            )
            self.__messages[-1].set_message_send_time(t_timestamp=timestamp)
            x = rng.exponential(scale=t_lambda, size=1)
            timestamp += x[0]
            msg_id += 1

    def get_client_id(self) -> int:
        return self.__id

    def has_messages(self) -> bool:
        return len(self.__messages) > 0

    def get_next_msg_time(self) -> float:
        assert self.has_messages()
        return self.__messages[0].get_message_send_time()

    def pop_message(self) -> Message:
        assert self.has_messages()
        return self.__messages.pop(0)

    def get_messages_count(self) -> int:
        return len(self.__messages)
