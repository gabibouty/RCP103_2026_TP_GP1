import numpy as np

from sources.scheduler import Scheduler
from sources.events_and_messages import Event, Message, EventType


def test_sheduler():
    sch: Scheduler = Scheduler()

    EVENT_COUNT = 10000

    random_x = np.random.default_rng(seed=1).uniform(
        low=0, high=EVENT_COUNT, size=EVENT_COUNT
    )
    for id, x in enumerate(random_x):
        event: Event = Event(id, EventType.SEND_MSG, x, Message(id, 1, 0))
        sch.add_event(event)

    assert sch.has_events()

    time: float = 0.0
    while sch.has_events():
        assert time <= sch.get_current_time()
        time = sch.pop_event().get_event_time()
