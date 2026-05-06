from sources.events_and_messages import Message, Event, EventType
from sources.trace import get_time_and_node


def test_get_time_and_node_event_SEND_MSG():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.SEND_MSG, 0.0, message)
    assert get_time_and_node(event) == (1, 0.0)

def test_get_time_and_node_event_RECV_MSG():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.RECV_MSG, 0.0, message)
    assert get_time_and_node(event) == (2, 1.1)

def test_get_time_and_node_event_MSG_DEPT():
    message = Message(1, 1, 2)
    message.set_message_send_time(0.0)
    message.set_message_arrival_time(1.1)
    message.set_message_server_time(2.6)

    event = Event(1, EventType.MSG_DEPT, 0.0, message)
    assert get_time_and_node(event) == (2, 2.6)



