import pytest
from sources.events_and_messages import Message, Event, EventType
from sources.trace import get_time_and_node


# A tester avec la commande : $ pytest test_trace.py
def test_get_time_and_node():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.SEND_MSG, 0.0, message)
    assert get_time_and_node(event) == (1, 0.0)
