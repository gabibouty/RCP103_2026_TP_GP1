import numpy as np

from sources.scheduler import Scheduler
from sources.events_and_messages import Event, Message, EventType


def test_sheduler():
    sch: Scheduler = Scheduler()

    EVENT_COUNT = 1000

    random_x = np.random.default_rng(seed=1).uniform(
        low=0.01, high=EVENT_COUNT, size=EVENT_COUNT
    )
    for id, x in enumerate(random_x):
        msg = Message(id, 1, 0)
        msg.set_message_send_time(x)
        event: Event = Event(id, EventType.SEND_MSG, msg)
        sch.add_event(event)

    assert sch.has_events()

    time: float = sch.get_current_time()
    while sch.has_events():
        e: Event = sch.pop_event()
        assert e.get_event_time() == sch.get_current_time()
        assert time < sch.get_current_time()
        time = sch.get_current_time()

    assert len(sch.get_passed_events()) == EVENT_COUNT
