from sources.events_and_messages import Message
from sources.client import Client


def test_client_init():
    client = Client(t_id=1, t_destination=2, t_average=1.0)

    assert client.get_client_id() == 1
    assert client.get_next_msg_time() == 0.0


def test_get_next_msg_time():
    client = Client(t_id=1, t_destination=2, t_average=1.0)

    next_msg_time = client.get_next_msg_time()
    assert next_msg_time == 0.0


def test_pop_message():
    client = Client(t_id=1, t_destination=2, t_average=1.0)
