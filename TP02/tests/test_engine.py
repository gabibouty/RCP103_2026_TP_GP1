from sources.engine import Engine


def test_engine_complete():
    SIMULATION_DURATION = 10000
    engine: Engine = Engine(SIMULATION_DURATION)
    assert not engine.has_finished()
    engine.run()
    assert engine.has_finished()
