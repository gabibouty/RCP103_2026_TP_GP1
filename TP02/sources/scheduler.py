from typing import List

from sources.events_and_messages import Event


class Scheduler:
    def __init__(self):
        self.__events: List[Event] = []
        self.__passed_events: List[Event] = []
        self.__time: float = 0

    def add_event(self, t_event: Event):
        i = len(self.__events) - 1
        while i >= 0 and self.__events[i].get_event_time() > t_event.get_event_time():
            i -= 1
        self.__events.insert(i + 1, t_event)
        assert len(self.__events) != 0

    def pop_event(self) -> Event:
        e: Event = self.__events.pop(0)
        self.__passed_events.append(e)
        self.__time = e.get_event_time()
        return e

    def get_current_time(self) -> float:
        return self.__time

    def has_events(self) -> bool:
        return len(self.__events) != 0

    def get_passed_events(self) -> List[Event]:
        return self.__passed_events
