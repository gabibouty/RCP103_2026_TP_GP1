from typing import List
import math

from sources.engine import Engine, TraceType
from sources.events_and_messages import Event, EventType


def test_engine_complete():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION)

    engine.run()

    events: List[Event] = engine.log(TraceType.EVENT_LIST)

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

    assert len(send_events) > len(recv_events)
    assert len(recv_events) > len(dept_events)
