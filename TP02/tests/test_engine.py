from typing import List
import math

from sources.engine import Engine, TraceType
from sources.events_and_messages import Event, EventType


def test_engine_complete():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION)
    message_count = engine.get_all_messages_count()

    assert not engine.has_finished()
    engine.run()
    assert engine.has_finished()

    events: List[Event] = engine.log(TraceType.EVENT_LIST)
    assert len(events) == 3 * message_count

    send_events: List[Event] = []
    recv_events: List[Event] = []
    dept_events: List[Event] = []
    for e in events:
        if e.get_event_type() == EventType.SEND_MSG:
            send_events.append(e)
        elif e.get_event_type() == EventType.RECV_MSG:
            recv_events.append(e)
        else:
            dept_events.append(e)

    assert len(send_events) == len(recv_events)
    assert len(send_events) == len(dept_events)

    for i in range(len(send_events)):
        send_event = send_events[i]
        recv_event = recv_events[i]
        dept_event = dept_events[i]
        assert (
            send_event.get_message().get_message_id()
            == recv_event.get_message().get_message_id()
        )
        assert (
            send_event.get_message().get_message_id()
            == dept_event.get_message().get_message_id()
        )
        assert math.isclose(
            send_event.get_event_time(), recv_event.get_event_time() - 1.0
        )
        assert recv_event.get_event_time() <= dept_event.get_event_time()

    assert engine.is_queue_empty()
