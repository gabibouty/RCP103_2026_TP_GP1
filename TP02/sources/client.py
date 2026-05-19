import numpy as np

from typing import List
from sources.events_and_messages import Message


class Client:
    def __init__(
        self,
        t_id: int,
        t_average: float,
    ):
        self.__id: int = t_id
        self.__average: float = t_average
        self.__random_generator = np.random.default_rng(seed=t_id)
        self.__next_message_time: float = 0.0

    def get_client_id(self) -> int:
        return self.__id

    def get_next_msg_time(self) -> float:
        return self.__next_message_time

    def pop_message(self) -> Message:
        message: Message = Message(t_source=self.__id, t_destination=0)
        message.set_message_send_time(t_timestamp=self.__next_message_time)
        self.__next_message_time += self.__random_generator.exponential(
            scale=(1.0 / self.__average)
        )
        return message
