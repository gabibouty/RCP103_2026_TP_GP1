import numpy as np

from typing import List
from sources.events_and_messages import Message


class Client:
    # There is 4 message by time unit
    __CLIENT_AVG_TIMES: List[int] = [4, 6, 8, 12]
    __avg_time_selector = 0

    def __get_average_time():
        Client.__avg_time_selector = (Client.__avg_time_selector + 1) % len(
            Client.__CLIENT_AVG_TIMES
        )
        return Client.__CLIENT_AVG_TIMES[Client.__avg_time_selector]

    def __init__(self, t_id: int):
        self.__id: int = t_id
        self.__average: float = Client.__get_average_time()
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
