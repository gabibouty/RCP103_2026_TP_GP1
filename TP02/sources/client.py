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
        self, t_id: int, t_destination, t_simulation_duration: float, t_lambda: float
    ):
        # TODO: generate Message list directly in Client __init__
        self.__id = t_id
        self.__messages = []
        timestamp = 0.0
        rng = np.random.default_rng(seed=1)
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

    # TODO: add a method to check if there is message
    def has_messages(self) -> bool:
        return len(self.__messages) > 0

    def get_next_msg_time(self) -> float:
        assert self.has_messages()
        return self.__messages[0].get_message_send_time()

    def pop_message(self) -> Message:
        assert self.has_messages()
        return self.__messages.pop(0)
