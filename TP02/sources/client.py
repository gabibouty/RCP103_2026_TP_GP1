import numpy as np

from typing import List
from sources.events_and_messages import Message


class Client:
    def __init__(self, t_id: int, t_avg_send_by_time_unit: int):
        self.__id: int = t_id
        self.__avg_send_by_time_unit: float = t_avg_send_by_time_unit
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
            scale=(1.0 / self.__avg_send_by_time_unit)
        )
        return message
