from sources.events_and_messages import Event, EventType, Message


def test_event_init():
    msg = Message(2, 3)
    msg.set_message_send_time(1.5)
    event = Event(10, EventType.SEND_MSG, msg)

    assert event.get_event_time() == 1.5
    assert event.get_event_type() == EventType.SEND_MSG
    Message.reset_ids()


def test_event_message_content():
    msg = Message(2, 3)
    event = Event(10, EventType.MSG_DEPT, msg)

    event_msg = event.get_message()

    assert event_msg.get_message_id() == 0
    assert event_msg.get_message_source() == 2
    assert event_msg.get_message_destination() == 3
    Message.reset_ids()


def test_event_str():
    msg = Message(2, 3)
    msg.set_message_send_time(5.5)
    event = Event(10, EventType.SEND_MSG, msg)
    Message.reset_ids()

    assert str(event) == (
        "Event:: Id: 10 | "
        "Type: EventType.SEND_MSG | "
        "Timestamp: 5.5 | "
        "Msg: Message:: Id: 0 | Source: 2 | Dest: 3"
    )
