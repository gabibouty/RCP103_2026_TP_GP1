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
        # TODO: generate Message list directly in Client __init__
        self.__id = t_id
        self.__messages = t_messages

    def get_client_id(self) -> int:
        return self.__id

    # TODO: remove this
    def get_messages(self) -> List[Message]:
        return self.__messages

    # TODO: add a method to check if there is message

    def get_next_msg_time(self) -> float:
        return self.__messages[0].get_message_send_time()

    def pop_message(self) -> Message:
        return self.__messages.pop(0)
