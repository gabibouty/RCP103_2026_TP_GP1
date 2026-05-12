from typing import List

from sources.engine import Engine, TraceType
from sources.events_and_messages import Event


def test_engine_complete():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION)
    assert not engine.has_finished()
    engine.run()
    assert engine.has_finished()

    events: List[Event] = engine.log(TraceType.EVENT_LIST)
    assert len(events) > 0
