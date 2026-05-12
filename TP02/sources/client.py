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
    def __init__(self, t_id: int, t_messages: List[Message]):
        self.__id = t_id
        self.__messages = t_messages

    def get_client_id(self) -> int:
        return self.__id

    def get_messages(self) -> List[Message]:
        return self.__messages

    def get_next_msg_time(self) -> float:
        return self.__messages[0].get_message_send_time()

    def pop_message(self) -> Message:
        return self.__messages.pop(0)
