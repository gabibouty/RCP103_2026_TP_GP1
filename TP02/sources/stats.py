from typing import List, Tuple
from collections import deque
import numpy as np

from sources.events_and_messages import Event, EventType


class SortedEvents:
    def __init__(self, t_events: List[Event]):
        self.__send_events: List[Event] = []
        self.__recv_events: List[Event] = []
        self.__dept_events: List[Event] = []
        for e in t_events:
            if e.get_event_type() == EventType.SEND_MSG:
                self.__send_events.append(e)
            elif e.get_event_type() == EventType.RECV_MSG:
                self.__recv_events.append(e)
            else:
                self.__dept_events.append(e)
        assert self.__is_valid()

    def __is_valid(self) -> bool:
        return (len(self.__send_events) >= len(self.__recv_events)) and (
            len(self.__recv_events) >= len(self.__dept_events)
        )

    def get_all_events_of_type(self, t_event_type: EventType) -> List[Event]:
        if t_event_type == EventType.SEND_MSG:
            return self.__send_events
        elif t_event_type == EventType.RECV_MSG:
            return self.__recv_events
        else:
            return self.__dept_events

    def get_associated_event(
        self, t_event: Event, t_associated_type: EventType
    ) -> Event:
        associated_list: List[Event] = None
        if t_associated_type == EventType.SEND_MSG:
            associated_list = self.__send_events
        elif t_associated_type == EventType.RECV_MSG:
            associated_list = self.__recv_events
        else:
            associated_list = self.__dept_events
        return next(
            filter(
                lambda x: x.get_message().get_message_id()
                == t_event.get_message().get_message_id(),
                associated_list,
            )
        )


def average_time_in_queue(t_events: List[Event]) -> float:
    sorted_events = SortedEvents(t_events)
    times = [
        e.get_event_time()
        - sorted_events.get_associated_event(e, EventType.RECV_MSG).get_event_time()
        for e in sorted_events.get_all_events_of_type(EventType.MSG_DEPT)
    ]
    return np.mean(times)


def maximum_waiting_time_in_queue(t_events: List[Event]) -> float:
    sorted_events = SortedEvents(t_events)
    times = [
        e.get_event_time()
        - sorted_events.get_associated_event(e, EventType.RECV_MSG).get_event_time()
        for e in sorted_events.get_all_events_of_type(EventType.MSG_DEPT)
    ]
    return max(times)


def total_messages_sended(t_events: List[Event], t_time: float) -> int:
    sorted_events = SortedEvents(t_events)
    count = 0
    for e in sorted_events.get_all_events_of_type(EventType.SEND_MSG):
        if e.get_event_time() > t_time:
            break
        count += 1
    return count


def total_messages_received(t_events: List[Event], t_time: float) -> int:
    sorted_events = SortedEvents(t_events)
    count = 0
    for e in sorted_events.get_all_events_of_type(EventType.RECV_MSG):
        if e.get_event_time() > t_time:
            break
        count += 1
    return count


def total_messages_still_in_transmission(t_events: List[Event], t_time: float) -> int:
    return total_messages_sended(t_events, t_time) - total_messages_received(
        t_events, t_time
    )


def total_messages_transmit(t_events: List[Event], t_time: float) -> int:
    sorted_events = SortedEvents(t_events)
    count = 0
    for e in sorted_events.get_all_events_of_type(EventType.MSG_DEPT):
        if e.get_event_time() > t_time:
            break
        count += 1
    return count


def __messages_in_queue_and_dropped_at(
    t_events: List[Event], t_queue_size: int, t_time: float
):
    queue = deque()
    dropped = 0

    for e in t_events:
        if e.get_event_time() > t_time:
            break
        if e.get_event_type() == EventType.RECV_MSG:
            if e.get_event_time() <= t_time:
                if len(queue) < t_queue_size:
                    queue.append(e.get_message().get_message_id())
                else:
                    dropped += 1
        elif e.get_event_type() == EventType.MSG_DEPT:
            if queue:
                queue.popleft()

    return len(queue), dropped


def messages_in_queue_at(t_events: List[Event], t_queue_size: int, t_time: float):
    return __messages_in_queue_and_dropped_at(t_events, t_queue_size, t_time)[0]


def messages_dropped_at(t_events: List[Event], t_queue_size: int, t_time: float):
    return __messages_in_queue_and_dropped_at(t_events, t_queue_size, t_time)[1]
