from typing import List
import math

from sources.engine import Engine, TraceType
from sources.events_and_messages import Event, EventType


def test_engine_with_flush():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION, True, 1, 1)

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

    assert len(send_events) == len(recv_events)
    assert len(recv_events) == len(dept_events)

    for i in range(len(events) - 1):
        assert events[i].get_event_time() <= events[i + 1].get_event_time()

    for i in range(len(dept_events)):
        dpt_event = dept_events[i]
        rcv_event = recv_events[i]
        send_event = send_events[i]

        assert (
            rcv_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert (
            send_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert rcv_event.get_event_time() <= dpt_event.get_event_time()
        assert send_event.get_event_time() <= rcv_event.get_event_time()


def test_engine_without_flush():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION, False, 1, 1)

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

    for i in range(len(events) - 1):
        assert events[i].get_event_time() <= events[i + 1].get_event_time()

    for dpt_event in dept_events:
        msg_id = dpt_event.get_message().get_message_id()
        rcv_event: Event = next(
            filter(lambda x: x.get_message().get_message_id() == msg_id, recv_events)
        )
        assert rcv_event != None
        assert rcv_event.get_event_time() <= dpt_event.get_event_time()

    for rcv_event in recv_events:
        msg_id = rcv_event.get_message().get_message_id()
        send_event: Event = next(
            filter(lambda x: x.get_message().get_message_id() == msg_id, send_events)
        )
        assert send_event != None
        assert rcv_event.get_event_time() == send_event.get_event_time() + 1


def test_engine_with_flush_and_multiple_server():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION, True, 1, 4)

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

    assert len(send_events) == len(recv_events)
    assert len(recv_events) == len(dept_events)

    for i in range(len(events) - 1):
        assert events[i].get_event_time() <= events[i + 1].get_event_time()

    for i in range(len(dept_events)):
        dpt_event = dept_events[i]
        rcv_event = recv_events[i]
        send_event = send_events[i]

        assert (
            rcv_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert (
            send_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert rcv_event.get_event_time() <= dpt_event.get_event_time()
        assert send_event.get_event_time() <= rcv_event.get_event_time()


def test_engine_with_flush_and_multiple_client():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION, True, 4, 1)

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

    assert len(send_events) == len(recv_events)
    assert len(recv_events) == len(dept_events)

    for i in range(len(events) - 1):
        assert events[i].get_event_time() <= events[i + 1].get_event_time()

    for i in range(len(dept_events)):
        dpt_event = dept_events[i]
        rcv_event = recv_events[i]
        send_event = send_events[i]

        assert (
            rcv_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert (
            send_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert rcv_event.get_event_time() <= dpt_event.get_event_time()
        assert send_event.get_event_time() <= rcv_event.get_event_time()


def test_engine_with_flush_and_multiple_server_and_client():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION, True, 4, 4)

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

    assert len(send_events) == len(recv_events)
    assert len(recv_events) == len(dept_events)

    for i in range(len(events) - 1):
        assert events[i].get_event_time() <= events[i + 1].get_event_time()

    for i in range(len(dept_events)):
        dpt_event = dept_events[i]
        rcv_event = recv_events[i]
        send_event = send_events[i]

        assert (
            rcv_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert (
            send_event.get_message().get_message_id()
            == dpt_event.get_message().get_message_id()
        )
        assert rcv_event.get_event_time() <= dpt_event.get_event_time()
        assert send_event.get_event_time() <= rcv_event.get_event_time()
