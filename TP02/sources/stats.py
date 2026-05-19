from typing import List, Dict

from sources.events_and_messages import Event, EventType


def average_time_in_queue(t_events: List[Event]) -> float:
    # [Msg_Id, [Time on RECV, Time on DEPT ?]]
    deltas: Dict[int, List[int]] = {}

    for e in t_events:
        msg_id = e.get_message().get_message_id()
        if e.get_event_type() == EventType.SEND_MSG:
            continue
        elif e.get_event_type() == EventType.RECV_MSG:
            assert msg_id not in deltas.keys()
            deltas[msg_id] = []
            deltas[msg_id].append(e.get_event_time())
        else:
            assert msg_id in deltas.keys()
            deltas[msg_id].append(e.get_event_time())

    sum = 0.0
    count = 0
    for msg_id, times in deltas.items():
        if len(times) == 2:
            sum += times[1] - times[0]
            count += 1
    return sum / count if count != 0 else 0


def maximum_waiting_messages_in_queue(t_events: List[Event]) -> int:
    pass


def total_messages_sended(t_events: List[Event]) -> int:
    pass


def total_messages_droped(t_events: List[Event]) -> int:
    pass


def total_messages_transmit(t_events: List[Event]) -> int:
    pass
