from typing import List

from events_and_messages import Event


class Scheduler:
    def __init__(self):
        self.__events: List[Event] = []

    def add_event(self, t_event: Event):
        i = len(self.__events) - 1
        while i >= 0 and self.__events[i].get_event_time() > t_event.get_event_time():
            i -= 1
        self.__events.insert(i + 1, t_event)

    def pop_event(self) -> Event:
        return self.__events.pop(0)

    def get_current_time(self) -> Event:
        return self.__events[-1].get_event_time()

    def has_events(self) -> bool:
        return len(self.__events) == 0
