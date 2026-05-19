from sources.events_and_messages import Message
from sources.client import Client


def test_client_init():
    client = Client(t_id=1)

    assert client.get_client_id() == 1
    assert client.get_next_msg_time() == 0.0


def test_get_next_msg_time():
    client = Client(t_id=1)

    next_msg_time = client.get_next_msg_time()
    assert next_msg_time == 0.0
    client.pop_message()
    assert next_msg_time < client.get_next_msg_time()


def test_pop_message():
    client = Client(t_id=1)
    time: float = client.pop_message().get_message_send_time()
    assert time == 0.0

    TEST_DURATION = 10000.0

    while time < TEST_DURATION:
        assert client.get_next_msg_time() > time
        time = client.get_next_msg_time()
        msg = client.pop_message()
        assert time == msg.get_message_send_time()
