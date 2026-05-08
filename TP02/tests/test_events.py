from sources.events_and_messages import Event, EventType, Message

def test_event_init():
    msg = Message(1,2,3)
    event = Event(10, EventType.SEND_MSG, 1.5, msg)

    assert event.get_event_time() == 1.5
    assert event.get_event_type() == EventType.SEND_MSG


def test_event_setters():
    msg = Message(1, 2, 3)
    event = Event(10, EventType.SEND_MSG, 5.5, msg)

    event.set_event_time(8.0)
    event.set_event_type(EventType.RECV_MSG)

    assert event.get_event_time() == 8.0
    assert event.get_event_type() == EventType.RECV_MSG


def test_event_message_content():
    msg = Message(1, 2, 3)
    event = Event(10, EventType.MSG_DEPT, 4.0, msg)

    event_msg = event.get_message()

    assert event_msg.get_message_id() == 1
    assert event_msg.get_message_source() == 2
    assert event_msg.get_message_destination() == 3


def test_event_str():
    msg = Message(1, 2, 3)
    event = Event(10, EventType.SEND_MSG, 5.5, msg)

    assert str(event) == (
        "Event:: Id: 10 | "
        "Type: EventType.SEND_MSG | "
        "Timestamp: 5.5 | "
        "Msg: Message:: Id: 1 | Source: 2 | Dest: 3"
    )