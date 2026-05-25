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
        result = next(
            filter(
                lambda x: x.get_message().get_message_id()
                == t_event.get_message().get_message_id(),
                associated_list,
            ),
            None,
        )
        return result


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
        if e.get_event_time() >= t_time:
            break
        count += 1
    return count


def total_messages_received(t_events: List[Event], t_time: float) -> int:
    sorted_events = SortedEvents(t_events)
    count = 0
    for e in sorted_events.get_all_events_of_type(EventType.RECV_MSG):
        if e.get_event_time() >= t_time:
            break
        count += 1
    return count


def messages_still_in_transmission_at(t_events: List[Event], t_time: float) -> int:
    return total_messages_sended(t_events, t_time) - total_messages_received(
        t_events, t_time
    )


def total_messages_transmit(t_events: List[Event], t_time: float) -> int:
    sorted_events = SortedEvents(t_events)
    count = 0
    for e in sorted_events.get_all_events_of_type(EventType.MSG_DEPT):
        if e.get_event_time() >= t_time:
            break
        count += 1
    return count


def __messages_in_queue_and_dropped_at(
    t_events: List[Event], t_queue_size: int, t_time: float
):
    queue = 0
    dropped = 0

    for e in t_events:
        if e.get_event_time() >= t_time:
            break

        if e.get_event_type() == EventType.RECV_MSG:
            if t_queue_size is None or queue < t_queue_size:
                queue += 1
            else:
                dropped += 1
        elif e.get_event_type() == EventType.MSG_DEPT:
            assert queue > 0
            queue -= 1

    return queue, dropped


def messages_in_queue_at(t_events: List[Event], t_queue_size: int, t_time: float):
    return __messages_in_queue_and_dropped_at(t_events, t_queue_size, t_time)[0]


def total_messages_dropped(t_events: List[Event], t_queue_size: int, t_time: float):
    return __messages_in_queue_and_dropped_at(t_events, t_queue_size, t_time)[1]


def mean_queue_size(
    t_events: List[Event], t_queue_size: int, t_end_time: float
) -> float:
    current_queue_size = 0  # la taille actuelle de la file d'attente
    previous_time = 0.0  # temps du dernier événement traité
    area = 0.0  # la somme des tailles de la file d'attente multipliées par les durées correspondantes

    for e in t_events:  # le temps de l'event courant
        current_time = e.get_event_time()

        duration = (
            current_time - previous_time
        )  # la durée où la file est restée avec la meme taille depuis le dernier event
        area += current_queue_size * duration

        if (
            e.get_event_type() == EventType.RECV_MSG
        ):  # si un msg arrive la taille augnmente
            if t_queue_size is None or current_queue_size < t_queue_size:
                current_queue_size += 1
        elif (
            e.get_event_type() == EventType.MSG_DEPT
        ):  # si msg quitte la taille diminue
            assert current_queue_size > 0
            current_queue_size -= 1

        previous_time = current_time  # on met à jour le temps du dernier event traité

    area += current_queue_size * (
        t_end_time - previous_time
    )  # on ajoute la dernière période, entre le dernier event et le temps étudié, multipliée par la taille actuelle de la file d'attente

    return area / t_end_time  # moyenne pondérée par le temps


def mean_request_in_system(
    t_events: List[Event], t_queue_size: int, t_end_time: float
) -> float:
    current_queue_size = 0
    current_in_transmission = 0
    previous_time = 0.0
    area = 0.0

    for e in t_events:
        current_time = e.get_event_time()

        duration = current_time - previous_time
        area += (current_queue_size + current_in_transmission) * duration

        if e.get_event_type() == EventType.SEND_MSG:
            current_in_transmission += 1
        elif e.get_event_type() == EventType.RECV_MSG:
            current_in_transmission -= 1
            if t_queue_size is None or current_queue_size < t_queue_size:
                current_queue_size += 1
        elif e.get_event_type() == EventType.MSG_DEPT:
            assert current_queue_size > 0
            current_queue_size -= 1

        previous_time = current_time

    area += (current_queue_size + current_in_transmission) * (
        t_end_time - previous_time
    )

    return area / t_end_time


def average_max_min_time_in_system(t_events: List[Event]) -> float:
    times = []
    sorted_events: SortedEvents = SortedEvents(t_events)
    for send_event in sorted_events.get_all_events_of_type(EventType.SEND_MSG):
        e = sorted_events.get_associated_event(send_event, EventType.MSG_DEPT)
        if e != None:
            times.append(e.get_event_time() - send_event.get_event_time())
            continue
        e = sorted_events.get_associated_event(send_event, EventType.RECV_MSG)
        if e != None:
            times.append(e.get_event_time() - send_event.get_event_time())
    return np.mean(times), max(times), min(times)


def rejection_rate(t_events: List[Event], t_queue_size: int, t_time: float) -> float:
    total_received = total_messages_received(t_events, t_time)
    if total_received == 0:  # pour éviter la division par zéro
        return 0.0
    dropped = total_messages_dropped(t_events, t_queue_size, t_time)
    return dropped / total_received
