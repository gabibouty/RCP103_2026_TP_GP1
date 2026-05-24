from typing import List
import math

from sources.engine import Engine, TraceType
from sources.events_and_messages import Event, EventType


def test_engine():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(
        t_simulation_duration=SIMULATION_DURATION,
        t_client_count=1,
        t_client_lambda=4,
        t_server_count=1,
        t_queue_limit=None,
    )

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


def test_engine_with_multiple_server():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(
        t_simulation_duration=SIMULATION_DURATION,
        t_client_count=1,
        t_client_lambda=4,
        t_server_count=4,
        t_queue_limit=None,
    )

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
    assert len(recv_events) >= len(dept_events)

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


def test_engine_with_multiple_client():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(
        t_simulation_duration=SIMULATION_DURATION,
        t_client_count=4,
        t_client_lambda=4,
        t_server_count=1,
        t_queue_limit=None,
    )

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


def test_engine_with_multiple_server_and_client():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(
        t_simulation_duration=SIMULATION_DURATION,
        t_client_count=4,
        t_client_lambda=4,
        t_server_count=4,
        t_queue_limit=None,
    )

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
