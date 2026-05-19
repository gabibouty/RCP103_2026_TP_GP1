from sources.stats import *
from sources.engine import Engine, TraceType


def test_avg_in_queue():
    SIMULATION_DURATION = 10
    engine: Engine = Engine(SIMULATION_DURATION, False, 2, 1, 4)
    engine.run()
    engine.log(TraceType.STDIO)
    avg_time = average_time_in_queue(engine.log(TraceType.EVENT_LIST))
    print(f"Avg time = {avg_time}")
    assert avg_time != 0.0
