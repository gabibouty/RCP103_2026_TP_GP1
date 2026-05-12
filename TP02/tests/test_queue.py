from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
import pytest


def test_put():
    message1 = Message(1, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(2, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, message1)
    event2 = Event(2, EventType.SEND_MSG, message2)

    queue = Queue()
    queue.put(event1)
    queue.put(event2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.index(event1) == 0
    assert queue.index(event2) == 1


def test_get():
    message1 = Message(1, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(2, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, message1)
    event2 = Event(2, EventType.SEND_MSG, message2)

    queue = Queue()
    queue.put(event1)
    queue.put(event2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.get() == event1
    assert queue.get() == event2
    with pytest.raises(IndexError, match="Queue is empty"):
        queue.get()


def test_is_empty():
    message1 = Message(1, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(2, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, message1)
    event2 = Event(2, EventType.SEND_MSG, message2)

    queue = Queue()
    queue.put(event1)
    queue.put(event2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.is_empty() == False
    queue.get()
    queue.get()
    assert queue.is_empty() == True


def test_size():
    message1 = Message(1, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(2, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, message1)
    event2 = Event(2, EventType.SEND_MSG, message2)

    queue = Queue()
    queue.put(event1)
    queue.put(event2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.size() == 2


def test_str():
    message1 = Message(1, 1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(2, 1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    event1 = Event(1, EventType.SEND_MSG, message1)
    event2 = Event(2, EventType.SEND_MSG, message2)

    queue = Queue()
    ret = str(queue)
    assert ret == "Size: 0\nElements : []"
    queue.put(event1)
    queue.put(event2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    ret = str(queue)
    assert (
        ret
        == "Size: 2\nElements : [Event:: Id: 1 | Type: EventType.SEND_MSG | Timestamp: 0.0 | Msg: Message:: Id: 1 | Source: 1 | Dest: 2, Event:: Id: 2 | Type: EventType.SEND_MSG | Timestamp: 0.2 | Msg: Message:: Id: 2 | Source: 1 | Dest: 3]"
    )
