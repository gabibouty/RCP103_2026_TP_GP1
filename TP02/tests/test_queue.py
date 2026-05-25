from sources.events_and_messages import Message, Event, EventType
from sources.queue import Queue
import pytest


def test_put():
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    queue = Queue()
    queue.put(message1)
    queue.put(message2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.index(message1) == 0
    assert queue.index(message2) == 1
    Message.reset_ids()


def test_get():
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    queue = Queue()
    queue.put(message1)
    queue.put(message2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.get() == message1
    assert queue.get() == message2
    with pytest.raises(IndexError, match="Queue is empty"):
        queue.get()
    Message.reset_ids()


def test_is_empty():
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    queue = Queue()
    queue.put(message1)
    queue.put(message2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.is_empty() == False
    queue.get()
    queue.get()
    assert queue.is_empty() == True
    Message.reset_ids()


def test_size():
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    queue = Queue()
    queue.put(message1)
    queue.put(message2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.size() == 2

    Message.reset_ids()


def test_str():
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    queue = Queue()
    ret = str(queue)
    assert ret == "Size: 0\nElements : []"
    queue.put(message1)
    queue.put(message2)

    # https://docs.pytest.org/en/6.2.x/capture.html
    ret = str(queue)
    assert (
        ret
        == "Size: 2\nElements : [Message:: Id: 0 | Source: 1 | Dest: 2, Message:: Id: 1 | Source: 1 | Dest: 3]"
    )

    Message.reset_ids()


def test_put_size1():
    message1 = Message(1, 2)
    message1.set_message_send_time(0.0)
    message1.set_message_arrival_time(1.1)
    message1.set_message_server_time(2.6)

    message2 = Message(1, 3)
    message2.set_message_send_time(0.2)
    message2.set_message_arrival_time(1.2)
    message2.set_message_server_time(4.6)

    message3 = Message(1, 3)
    message3.set_message_send_time(0.2)
    message3.set_message_arrival_time(1.2)
    message3.set_message_server_time(4.6)

    queue = Queue(1)
    queue.put(message1)
    queue.put(message2)
    queue.put(message3)

    # https://docs.pytest.org/en/6.2.x/capture.html
    assert queue.index(message1) == 0
    assert queue.size() == 1
    Message.reset_ids()
