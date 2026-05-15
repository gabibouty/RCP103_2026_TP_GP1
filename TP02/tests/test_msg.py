from sources.events_and_messages import Message


def test_message():
    msg = Message(1, 2, 3)
    assert msg.get_message_id() == 1
    assert msg.get_message_source() == 2
    assert msg.get_message_destination() == 3

    assert msg.get_message_send_time() == 0
    assert msg.get_message_arrival_time() == 0
    assert msg.get_message_server_time() == 0


def test_message_setters():
    msg = Message(1, 2, 3)
    msg.set_message_id(10)
    msg.set_message_source(20)
    msg.set_message_destination(30)
    msg.set_message_send_time(1.5)
    msg.set_message_arrival_time(2.5)
    msg.set_message_server_time(3.5)

    assert msg.get_message_id() == 10
    assert msg.get_message_source() == 20
    assert msg.get_message_destination() == 30
    assert msg.get_message_send_time() == 1.5
    assert msg.get_message_arrival_time() == 2.5
    assert msg.get_message_server_time() == 3.5


def test_message_str():
    msg = Message(1, 2, 3)
    assert str(msg) == "Message:: Id: 1 | Source: 2 | Dest: 3"
